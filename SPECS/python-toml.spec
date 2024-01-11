# Disable tests on RHEL9 as to not pull in the test dependencies
# Specify --with tests to run the tests e.g. on EPEL
%bcond_with tests

%global pypi_name toml
%global desc TOML aims to be a minimal configuration file format that's easy to read due to \
obvious semantics. TOML is designed to map unambiguously to a hash table. TOML \
should be easy to parse into data structures in a wide variety of languages. \
This package loads toml file into python dictionary and dump dictionary into \
toml file.

Name:           python-%{pypi_name}
Version:        0.10.2
Release:        6%{?dist}
Summary:        Python Library for Tom's Obvious, Minimal Language

License:        MIT
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        %{pypi_source}

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  pyproject-rpm-macros

%if %{with tests}
BuildRequires:  /usr/bin/toml-test
%endif

%description
%desc


%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
%desc


%prep
%autosetup -p1 -n %{pypi_name}-%{version}
# https://github.com/uiri/toml/pull/339
sed -i '/pytest-cov/d' tox.ini


%generate_buildrequires
%pyproject_buildrequires %{?with_tests:-t}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{pypi_name}


%if %{with tests}
%check
ln -s /usr/share/toml-test/ .  # python tests require test cases here
%tox
# Also using the language independent toml-test suite to launch tests
ln -s /usr/share/toml-test/tests/* tests/  # toml-test requires them here
toml-test $(pwd)/tests/decoding_test3.sh
%endif


%files -n python%{python3_pkgversion}-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.rst


%changelog
* Tue Feb 08 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 0.10.2-6
- Add automatically generated Obsoletes tag with the python39- prefix
  for smoother upgrade from RHEL8
- Related: rhbz#1990421

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 0.10.2-5
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 0.10.2-4
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Wed Mar 10 2021 Charalampos Stratakis <cstratak@redhat.com> - 0.10.2-3
- Disable tests on RHEL9 to avoid pulling in the test dependencies

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.10.2-1
- Update to 0.10.2
- Fixes: rhbz#1893498

* Fri Nov 13 2020 Miro Hrončok <mhroncok@redhat.com> - 0.10.1-4
- Don't BR pytest-cov

* Thu Sep 03 2020 Miro Hrončok <mhroncok@redhat.com> - 0.10.1-3
- Use pyproject-rpm-macros

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 19 2020 Miro Hrončok <mhroncok@redhat.com> - 0.10.1-1
- Update to 0.10.1 (#1835567)

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-8
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 11 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-3
- Subpackage python2-toml has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 25 2018 Julien Enselme <jujens@jujens.eu> - 0.10.0-1
- Update to 0.10.0 (#1652946)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.4-4
- Rebuilt for Python 3.7

* Wed Feb 21 2018 Sayan Chowdhury <sayanchowdhury@fedoraproject.org> - 0.9.4-3
- Make changes to build the package for EPEL

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 27 2017 Julien Enselme <jujens@jujens.eu> - 0.9.4-1
- Update to 0.9.4

* Tue Sep 26 2017 Julien Enselme <jujens@jujens.eu> - 0.9.3-1
- Update to 0.9.3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9.2-2
- Rebuild for Python 3.6

* Thu Sep 01 2016 Julien Enselme <jujens@jujens.eu> - 0.9.2-1
- Update to 0.9.2
- Improve spec with %%summary and %%desc macros

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 11 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov 9 2015 Julien Enselme <jujens@jujens.eu> - 0.9.1-4
- Correct %%python_provides for python3

* Thu Nov 5 2015 Julien Enselme <jujens@jujens.eu> - 0.9.1-3
- Rebuilt for python 3.5

* Sat Aug 8 2015 Julien Enselme <jujens@jujens.eu> - 0.9.1-2
- Enable tests suite
- Build python3 and python2 in the same directory
- Use %%py2_build, %%py3_build, %%py2_install and %%py2_install
- Move python2 package in its own subpackage

* Sat Jul 11 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.9.1-1
- Update to 0.9.1 (#1242131)

* Sun Jun 28 2015 Julien Enselme <jujens@jujens.eu> - 0.9.0-2
- Update description to explain what toml is
- Try to import the package in %%check

* Mon Jun 15 2015 Julien Enselme <jujens@jujens.eu> - 0.9.0-1
- Initial packaging
