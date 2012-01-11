%define		pkg	klass
Summary:	Utility for creating expressive classes in JavaScript
Name:		js-%{pkg}
Version:	1.0
Release:	2
License:	MIT
Group:		Applications/WWW
Source0:	https://github.com/ded/klass/tarball/v1.0/%{pkg}-%{version}.tgz
# Source0-md5:	0bd574d1cfa02ffee98af466b9ec3491
URL:		http://www.dustindiaz.com/klass
BuildRequires:	rpmbuild(macros) >= 1.461
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
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

# apache1/apache2 conf
cat > apache.conf <<'EOF'
Alias /js/klass %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

# lighttpd conf
cat > lighttpd.conf <<'EOF'
alias.url += (
    "/js/klass" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -p %{pkg}.js $RPM_BUILD_ROOT%{_appdir}/%{pkg}-%{version}.js
cp -p %{pkg}.min.js $RPM_BUILD_ROOT%{_appdir}/%{pkg}-%{version}.min.js
ln -s %{pkg}-%{version}.min.js $RPM_BUILD_ROOT%{_appdir}/%{pkg}.js

cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
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
