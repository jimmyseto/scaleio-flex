Name:           DellEMC-ScaleIO-flexvolume
Version:        0.1.0
Release:        1
Summary:        FlexVolume driver for ScaleIO 
URL:            http://www.emc.com/
Source0:        https://www.github.com/eric-young/scaleio-flex
License:        none

%global flexdir /usr/libexec/kubernetes/kubelet-plugins/volume/exec
%global instdir /opt/emc/scaleio/flexvolume

%description
FlexVolume driver for ScaleIO

%prep
%setup -n

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{instdir}
mkdir -p $RPM_BUILD_ROOT%{flexdir}/dell~scaleio
mkdir -p $RPM_BUILD_ROOT%{flexdir}/dell~scaleio-simple
cp -a scaleio $RPM_BUILD_ROOT%{instdir}
cp -a scaleio-simple $RPM_BUILD_ROOT%{instdir}
cp -a get-token.sh $RPM_BUILD_ROOT%{instdir}

%post
ln -s -f %{instdir}/scaleio %{flexdir}/dell~scaleio/scaleio 
ln -s -f %{instdir}/scaleio-simple %{flexdir}/dell~scaleio-simple/scaleio-simple

%pre

%preun

%postun
%{__rm} -f %{flexdir}/dell~scaleio/scaleio
%{__rm} -f %{flexdir}/dell~scaleio/scaleio-simple

%clean

%files
%{instdir}/scaleio
%{instdir}/scaleio-simple
%{instdir}/get-token.sh
%dir %{flexdir}/dell~scaleio
%dir %{flexdir}/dell~scaleio-simple

%defattr(744, root, root, -)

%doc
