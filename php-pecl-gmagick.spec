%global	php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?__pecl:		%{expand:	%%global __pecl	%{_bindir}/pecl}}
%{!?php_extdir:	%{expand:	%%global php_extdir	%(php-config --extension-dir)}}

%define	peclName	gmagick

Summary:		Provides a wrapper to the GraphicsMagick library
Name:		php-pecl-%peclName
Version:		1.1.0RC2
Release:		1%{?dist}
License:		PHP
Group:		Development/Libraries
Source0:		http://pecl.php.net/get/%peclName-%{version}.tgz
Source1:		%peclName.ini
# It is for EPEL too, so BuildRoot stil needed
BuildRoot:	%{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
URL:			http://pecl.php.net/package/%peclName
BuildRequires:	php-pear >= 1.4.7
BuildRequires: php-devel >= 5.1.3, GraphicsMagick-devel >= 1.2.6
Requires(post):	%{__pecl}
Requires(postun):	%{__pecl}
%if 0%{?php_zend_api:1}
Requires:		php(zend-abi) = %{php_zend_api}
Requires:		php(api) = %{php_core_api}
%else
Requires:		php-api = %{php_apiver}
%endif
Provides:		php-pecl(%peclName) = %{version}

Conflicts:	php-pecl-imagick

%description
%peclName is a php extension to create, modify and obtain meta information of
images using the GraphicsMagick API.

%prep
%setup -qc

%build
cd %peclName-%{version}
phpize
%{configure} --with-%peclName
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

cd %peclName-%{version}

make install \
	INSTALL_ROOT=%{buildroot}

# Install XML package description
install -m 0755 -d %{buildroot}%{pecl_xmldir}
install -m 0664 ../package.xml %{buildroot}%{pecl_xmldir}/%peclName.xml
install -d %{buildroot}%{_sysconfdir}/php.d/
install -m 0664 %{SOURCE1} %{buildroot}%{_sysconfdir}/php.d/%peclName.ini

chmod 0644 README

%check
# simple module load test
php --no-php-ini --define extension=./%peclName-%{version}/modules/gmagick.so \
	--modules | grep %peclName

%clean
rm -rf %{buildroot}

%post
%if 0%{?pecl_install:1}
%{pecl_install} %{pecl_xmldir}/%peclName.xml
%endif

%postun
%if 0%{?pecl_uninstall:1}
if [ "$1" -eq "0" ]; then
	%{pecl_uninstall} %peclName
fi
%endif

%files
%defattr(-,root,root,-)
%doc %peclName-%{version}/{README,LICENSE}
%{_libdir}/php/modules/%peclName.so
%{pecl_xmldir}/%peclName.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/php.d/%peclName.ini

%changelog
* Sat Mar 10 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 1.1.0RC2-1
- Update to 1.1.0RC2 by request bz#751376

* Mon Sep 12 2011 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.7b1-9
- Fix FBFS f16-17. Bz#716217

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7b1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 10 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.7b1-7
- Update to 1.0.7b1 version due to previous mentioned bug.

* Tue Aug 10 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.5b1-6
- Add simple %%check section by suggestion from Remi Collet (http://pecl.php.net/bugs/17991).

* Mon Jul 26 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.5b1-5
- Update to 1.0.5b1
- Add Conflicts: php-pecl-imagick - BZ#559675

* Sun Jan 31 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.3b3-4
- Update to 1.0.3b3

* Tue Nov 3 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.2b1-3
- Fedora Review started, thanks to Andrew Colin Kissa.
- Remove macros %%{__make} in favour to plain make.
- Add %%{?_smp_mflags} to make.

* Mon Oct 12 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.2b1-2
- New version 1.0.2b1 - author include license text by my request. Thank you Vito Chin.
- Include LICENSE.

* Fri Oct 2 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 1.0.1b1-1
- Initial release.
- License text absent, but I ask Vito Chin by email to add it into tarball.