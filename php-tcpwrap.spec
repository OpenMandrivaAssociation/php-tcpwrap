%define modname tcpwrap
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A24_%{modname}.ini

Summary:	Tcpwrappers bindings for PHP
Name:		php-%{modname}
Version:	1.0
Release:	%mkrel 13
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/tcpwrap
Source0:	%{modname}-%{version}.tar.bz2
Source1:	%{modname}.ini.bz2
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	tcp_wrappers-devel
Requires:	tcp_wrappers
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
This package handles /etc/hosts.allow and /etc/hosts.deny files.

%prep

%setup -q -n %{modname}-%{version}

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

cat > README.%{modname} << EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
EOF

bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
