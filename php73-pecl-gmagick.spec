# IUS spec file for php73-pecl-gmagick, forked from:
#
# Fedora spec file for php-pecl-gmagick
#
%global pecl_name  gmagick
%global prever     RC1
%global ini_name   40-%{pecl_name}.ini
%global php        php73

%bcond_with zts

Summary:        Provides a wrapper to the GraphicsMagick library
Name:           %{php}-pecl-%{pecl_name}
Version:        2.0.4
Release:        0.10.%{prever}%{?dist}
Source0:        https://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz
Source1:        %{pecl_name}.ini
License:        PHP
Group:          System Environment/Libraries
URL:            https://pecl.php.net/package/%{pecl_name}

BuildRequires:  %{php}-devel
BuildRequires:  GraphicsMagick-devel >= 1.3.17

BuildRequires:  pear1u
# explicitly require pear dependencies to avoid conflicts
BuildRequires:  %{php}-cli
BuildRequires:  %{php}-common
BuildRequires:  %{php}-process
BuildRequires:  %{php}-xml

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

Provides:       php-pecl(%{pecl_name}) = %{version}

Conflicts:      php-pecl-imagick
Conflicts:      php-magickwand

# safe replacement
Provides:       php-pecl-%{pecl_name} = %{version}-%{release}
Provides:       php-pecl-%{pecl_name}%{?_isa} = %{version}-%{release}
Conflicts:      php-pecl-%{pecl_name} < %{version}-%{release}

%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{php_ztsextdir}/.*\.so$}
%{?filter_setup}


%description
%{pecl_name} is a php extension to create, modify and obtain meta information of
images using the GraphicsMagick API.


%prep
%setup -qc
mv %{pecl_name}-%{version}%{?prever} NTS

sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml

extver=$(sed -n '/#define PHP_GMAGICK_VERSION/{s/.* "//;s/".*$//;p}' NTS/php_gmagick.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi

%if %{with zts}
cp -r NTS ZTS
%endif

%build
pushd NTS
%{_bindir}/phpize
%{configure} \
  --with-%{pecl_name}=%{prefix} \
  --with-php-config=%{_bindir}/php-config
%make_build
popd

%if %{with zts}
pushd ZTS
%{_bindir}/zts-phpize
%configure \
  --with-%{pecl_name}=%{prefix} \
  --with-php-config=%{_bindir}/zts-php-config
%make_build
popd
%endif

%install
make install INSTALL_ROOT=%{buildroot} -C NTS

# Install configuration file
install -D -m 644 %{SOURCE1} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -p -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{pecl_name}.xml

%if %{with zts}
make install INSTALL_ROOT=%{buildroot} -C ZTS
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do [ -f NTS/$i ] && install -D -p -m 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
export REPORT_EXIT_STATUS=1

pushd NTS
%{__php} --no-php-ini \
    --define extension_dir=%{buildroot}%{php_extdir} \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}

TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
NO_INTERACTION=1 \
%{__php} -n run-tests.php --show-diff
popd

%if %{with zts}
%{__ztsphp} --no-php-ini \
    --define extension_dir=%{buildroot}%{php_ztsextdir} \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


%triggerin -- pear1u
if [ -x %{__pecl} ]; then
    %{pecl_install} %{pecl_xmldir}/%{pecl_name}.xml >/dev/null || :
fi


%posttrans
if [ -x %{__pecl} ]; then
    %{pecl_install} %{pecl_xmldir}/%{pecl_name}.xml >/dev/null || :
fi


%postun
if [ $1 -eq 0 -a -x %{__pecl} ]; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%license NTS/LICENSE
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{pecl_name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif

%changelog
* Wed May 01 2019 Matt Linscott <matt.linscott@gmail.com> - 2.0.4-0.10.RC1
- Port from Fedora to IUS
- Remove pear requirement and add scriptlets (adapted from remirepo)
- Enable tests
- Split build in seperate NTS/ZTS builds
- Add version check against header
- Clean up installs and documentation

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-0.10.RC1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 11 2018 Remi Collet <remi@remirepo.net> - 2.0.4-0.9.RC1
- Rebuild for https://fedoraproject.org/wiki/Changes/php73

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-0.8.RC1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-0.7.RC1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 03 2017 Remi Collet <remi@fedoraproject.org> - 2.0.4-0.6.RC1
- rebuild for https://fedoraproject.org/wiki/Changes/php72

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-0.5.RC1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-0.4.RC1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-0.3.RC1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 14 2016 Remi Collet <remi@fedoraproject.org> - 2.0.4-0.2.RC1
- rebuild for https://fedoraproject.org/wiki/Changes/php71

* Mon Jun 27 2016 Remi Collet <remi@fedoraproject.org> - 2.0.4-0.1.RC1
- update to 2.0.4RC1
- rebuild for https://fedoraproject.org/wiki/Changes/php70
- spec cleanup
- fix license installation

* Thu Feb 25 2016 Remi Collet <remi@fedoraproject.org> - 1.1.7-0.6.RC2
- drop scriptlets (replaced by file triggers in php-pear #1310546)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-0.5.RC2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 05 2015 Rex Dieter <rdieter@fedoraproject.org> 1.1.7-0.4.RC2
- rebuild (GraphicsMagick)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-0.3.RC2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-0.2.RC2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> - 1.1.7-0.1.RC2
- update to 1.1.7RC2
- rebuild for https://fedoraproject.org/wiki/Changes/Php56
- add numerical prefix to extension configuration file

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.10.RC2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.9.RC2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 22 2013 Remi Collet <rcollet@redhat.com> - 1.1.0-0.8.RC2
- rebuild for http://fedoraproject.org/wiki/Features/Php55

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.7.RC2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 24 2012 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-0.6.
- rebuild (GraphicsMagick)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.5.RC2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 26 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 1.1.0-0.4.RC2
- Made pecl installation/deinstallation silent (bz#804919).

* Sat Mar 17 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 1.1.0-0.3.RC2
- Check module loading also for epel in single way. Thanks to Remi Collet for the hint.

* Sat Mar 10 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 1.1.0-0.2.RC2
- Skip %%check on epel5.

* Sat Mar 10 2012 Pavel Alexeev <Pahan@Hubbitus.info> - 1.1.0-0.1.RC2
- Update to 1.1.0RC2 by request bz#751376

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.0.10-0.1.b1
- update to 1.0.10b1 for php 5.4
- add filter to avoid private-shared-object-provides

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7b1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

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
