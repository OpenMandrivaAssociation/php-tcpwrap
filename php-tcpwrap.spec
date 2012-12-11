%define modname tcpwrap
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A24_%{modname}.ini

Summary:	Tcpwrappers bindings for PHP
Name:		php-%{modname}
Version:	1.1.3
Release:	%mkrel 21
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/tcpwrap
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Source1:	%{modname}.ini
Patch0:		tcpwrap-1.1.3-php54x.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	tcp_wrappers-devel
Requires:	tcp_wrappers
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This package handles /etc/hosts.allow and /etc/hosts.deny files.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%patch0 -p0

cp %{SOURCE1} %{inifile}

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

cat > README.%{modname} << EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
EOF

install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

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
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc README* package*.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-21mdv2012.0
+ Revision: 796992
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-20
+ Revision: 761334
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-19
+ Revision: 696479
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-18
+ Revision: 695474
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-17
+ Revision: 646693
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-16mdv2011.0
+ Revision: 629884
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-15mdv2011.0
+ Revision: 628198
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-14mdv2011.0
+ Revision: 600539
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-13mdv2011.0
+ Revision: 588876
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-12mdv2010.1
+ Revision: 514673
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-11mdv2010.1
+ Revision: 485491
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-10mdv2010.1
+ Revision: 468262
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-9mdv2010.0
+ Revision: 451364
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1:1.1.3-8mdv2010.0
+ Revision: 397618
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-7mdv2010.0
+ Revision: 377034
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-6mdv2009.1
+ Revision: 346643
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-5mdv2009.1
+ Revision: 341824
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-4mdv2009.1
+ Revision: 323110
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-3mdv2009.1
+ Revision: 310314
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-2mdv2009.0
+ Revision: 238435
- rebuild

* Thu Jul 17 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.3-1mdv2009.0
+ Revision: 236807
- 1.1.3

* Mon Jul 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.2-1mdv2009.0
+ Revision: 232350
- 1.1.2

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-15mdv2009.0
+ Revision: 200276
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-14mdv2008.1
+ Revision: 162250
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-13mdv2008.1
+ Revision: 107729
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-12mdv2008.0
+ Revision: 77584
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-11mdv2008.0
+ Revision: 39529
- use distro conditional -fstack-protector

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-10mdv2008.0
+ Revision: 21361
- rebuilt against new upstream version (5.2.2)


* Fri Mar 30 2007 Olivier Blin <oblin@mandriva.com> 1.0-9mdv2007.1
+ Revision: 149959
- rebuild because of binary package loss

* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-8mdv2007.1
+ Revision: 117635
- rebuilt against new upstream version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-7mdv2007.0
+ Revision: 78110
- rebuilt for php-5.2.0
- Import php-tcpwrap

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-6
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-5mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0-4mdk
- rebuilt for php-5.1.3

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-3mdk
- rebuilt against php-5.1.2

* Wed Nov 30 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-2mdk
- rebuilt against php-5.1.1

* Sat Nov 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.0-1mdk
- rebuilt against php-5.1.0
- fix versioning

* Sun Oct 02 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_1.0-0.RC1.1mdk
- rebuilt against php-5.1.0RC1

* Wed Sep 07 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.5_1.0-1mdk
- rebuilt against php-5.0.5 (Major security fixes)

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_1.0-1mdk
- rename the package

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_1.0-1mdk
- 5.0.4

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_1.0-2mdk
- use the %%mkrel macro

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_1.0-1mdk
- initial Mandrakelinux package

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_1.0-3mdk
- rebuilt against a non hardened-php aware php lib

* Sat Jan 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_1.0-2mdk
- rebuild due to hardened-php-0.2.6
- cleanups

* Thu Dec 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_1.0-1mdk
- rebuild for php 4.3.10

* Sat Oct 02 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.9_1.0-1mdk
- rebuild for php 4.3.9

* Thu Jul 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_1.0-1mdk
- rebuilt for php-4.3.8

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_1.0-2mdk
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_1.0-1mdk
- rebuilt for php-4.3.7

* Mon May 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_1.0-2mdk
- use the %%configure2_5x macro
- move scandir to /etc/php.d

* Thu May 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_1.0-1mdk
- built for php 4.3.6

