%define _cross_target m68k-apple-aux
Summary: Non-free system files from A/UX
Name: %{_cross_target}-nonfree
Version: 3.0.1
Release: 1
License: Proprietary
Group: Development/Languages
# URL: 
Source0: %{name}-%{version}.tar.Z
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch

%description
System libraries and headers required to cross-compile for A/UX.

%prep 
%setup -q -c
pushd usr/include >/dev/null
rm -f syslog.h
ln -s sys/syslog.h
popd >/dev/null
%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{_cross_target}/include
cp -a usr/include/* $RPM_BUILD_ROOT%{_prefix}/%{_cross_target}/include/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_prefix}/%{_cross_target}/include

%changelog
* Mon Sep  6 2021 jacob berkman <jacob@87k.net> 3.0.1-1
- Initial build.


