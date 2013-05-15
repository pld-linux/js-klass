%define		pkg	klass
Summary:	Class provider with classical inheritance interface
Name:		js-%{pkg}
Version:	1.2.2
Release:	3
License:	MIT
Group:		Applications/WWW
Source0:	https://github.com/ded/klass/tarball/master/%{pkg}-%{version}.tgz
# Source0-md5:	82df3cdf7b1a0f468f2bb5e4d48fa6c6
Source1:	apache.conf
Source2:	lighttpd.conf
Source3:	httpd.conf
URL:		http://www.dustindiaz.com/klass
BuildRequires:	rpmbuild(macros) >= 1.461
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Conflicts:	apache-base < 2.4.0-1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{name}

%description
An expressive, cross platform JavaScript Class provider with a
classical interface to prototypal inheritance.

%prep
%setup -qc
mv *-%{pkg}-*/* .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -p %{pkg}.js $RPM_BUILD_ROOT%{_appdir}/%{pkg}-%{version}.js
cp -p %{pkg}.min.js $RPM_BUILD_ROOT%{_appdir}/%{pkg}-%{version}.min.js
ln -s %{pkg}-%{version}.min.js $RPM_BUILD_ROOT%{_appdir}/%{pkg}.js

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README.md
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%{_appdir}
