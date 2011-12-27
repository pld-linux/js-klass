%define		pkg	klass
Summary:	Utility for creating expressive classes in JavaScript
Name:		js-%{pkg}
Version:	1.0
Release:	1
License:	MIT
Group:		Applications/WWW
Source0:	https://github.com/ded/klass/tarball/v1.0/%{pkg}-%{version}.tgz
# Source0-md5:	0bd574d1cfa02ffee98af466b9ec3491
URL:		http://www.dustindiaz.com/klass
BuildRequires:	rpmbuild(macros) >= 1.461
Requires:	js-webapps-common >= 1.0-1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/js/%{pkg}

%description
An expressive, cross platform JavaScript Class provider with a
classical interface to prototypal inheritance.

%prep
%setup -qc
mv *-%{pkg}-*/* .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}
cp -p %{pkg}.js $RPM_BUILD_ROOT%{_appdir}/%{pkg}-%{version}.js
cp -p %{pkg}.min.js $RPM_BUILD_ROOT%{_appdir}/%{pkg}-%{version}.min.js
ln -s %{pkg}-%{version}.min.js $RPM_BUILD_ROOT%{_appdir}/%{pkg}.js

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%{_appdir}
