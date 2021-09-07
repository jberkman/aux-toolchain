%global __os_install_post %{nil}
%define _cross_target m68k-apple-aux
Summary: A/UX system libraries
Name: %{_cross_target}-libs
Version: 3.0.1
Release: 1
License: Proprietary
Group: Development/Languages
# URL: 
Source0: aux-libs-%{version}.tar.Z
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch

%description
System libraries required to cross-compile for A/UX.

%prep 
%setup -q -c

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_prefix}/%{_cross_target}/lib
%{__cp} -a lib/* usr/lib/* $RPM_BUILD_ROOT%{_prefix}/%{_cross_target}/lib/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_prefix}/%{_cross_target}/lib

%changelog
* Mon Sep  6 2021 jacob berkman <jacob@87k.net> 3.0.1-1
- Initial build.


