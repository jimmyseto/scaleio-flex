Name:           DellEMC-ScaleIO-flexvolume
Version:        0.1.0
Release:        4
Summary:        FlexVolume driver for ScaleIO
URL:            http://www.emc.com/
Source0:        https://www.github.com/
License:        ASL 2.0
BuildArch:      noarch

# list of drivers to install
%global drivers scaleio

# global settings
%global flexdir /usr/libexec/kubernetes/kubelet-plugins/volume/exec
%global instdir /opt/emc/scaleio/flexvolume
%global logrotatedir /etc/logrotate.d
%global bindir %{instdir}/bin
%global cfgdir %{instdir}/cfg
%global instlog %{instdir}/install.log

%description
FlexVolume driver for ScaleIO

%prep
%setup -n

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{bindir}
install -d $RPM_BUILD_ROOT%{cfgdir}
install -d $RPM_BUILD_ROOT%{logrotatedir}
install -m 0666 LICENSE $RPM_BUILD_ROOT%{instdir}
install -m 0755 get-token.sh $RPM_BUILD_ROOT%{bindir}
install -m 0755 cfg/config.sample $RPM_BUILD_ROOT%{cfgdir}
install -m 0444 changes $RPM_BUILD_ROOT%{instdir}
install -m 0644 logrotate.d/DellEMC-ScaleIO-flexvolume $RPM_BUILD_ROOT%{logrotatedir}
for d in %{drivers}; do
  install -d $RPM_BUILD_ROOT%{flexdir}/dell~${d}
  install -m 0755 ${d} $RPM_BUILD_ROOT%{bindir}
done


%post
for d in %{drivers}; do
  ln -s -f %{bindir}/${d} %{flexdir}/dell~${d}/${d}
done

# see if the config file exists
# if not, just create it and we are done
echo "Processing configuration file" >> %instlog
if [ ! -f %{cfgdir}/config ]; then
  cp %{cfgdir}/config.sample %{cfgdir}/config
else
  CONFIG=%{cfgdir}/config
  CONFIG_OLD=%{cfgdir}/config.old
  CONFIG_NEW=%{cfgdir}/config.new

  # the config file exists
  cp %{cfgdir}/config.sample "${CONFIG_NEW}"
  cp %{cfgdir}/config "${CONFIG_OLD}"

  while read line
  do
    if [[ ${line:0:1} == [[:alnum:]] ]]
    then
      key=${line%=*}
      newline=$(grep "^${key}=" "${CONFIG_NEW}")
      if [ -z "${newline}" ]
      then
        echo "Found deprecated key: ${line}" >> %instlog
      elif [ "${newline}" != "${line}" ]
      then
        echo "Replacing: ${newline}"  >> %instlog
        echo "   with current value: ${line}"  >> %instlog
        sed -i "s|^${key}=.*|${line}|g" "${CONFIG_NEW}"
      fi
    fi
  done < "${CONFIG_OLD}"

  # done processing the file
  mv "${CONFIG_NEW}" "${CONFIG}"
fi

%pre

%preun

%postun
for d in %{drivers}; do
  if [ ! -f %{bindir}/${d} ]; then
    %{__rm} -f %{flexdir}/dell~${d}/${d}
  fi
done

%clean

%files
%{instdir}/LICENSE
%{instdir}/changes
%{bindir}/scaleio
%{bindir}/get-token.sh
%{cfgdir}/config.sample
%{logrotatedir}/DellEMC-ScaleIO-flexvolume
%dir %{flexdir}/dell~scaleio
%dir %{cfgdir}

%doc
