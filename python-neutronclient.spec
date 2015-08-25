Name:       python-neutronclient
Version:    2.3.4
Release:    1%{?dist}
Summary:    Python API and CLI for OpenStack Neutron

Group:      Development/Languages
License:    ASL 2.0
URL:        http://launchpad.net/python-neutronclient/
Source0:    https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

#
# patches_base=2.3.4
#
#Patch0001: 0001-Remove-runtime-dependency-on-python-pbr.patch

BuildArch:  noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr
BuildRequires: python-d2to1

Requires: pyparsing
Requires: python-httplib2
Requires: python-cliff >= 1.0
Requires: python-prettytable >= 0.6
Requires: python-setuptools
Requires: python-simplejson

%description
Client library and command line utility for interacting with Openstack
Neutron's API.

%prep
%setup -q -n %{name}-%{version}

#%patch0001 -p1

# We provide version like this in order to remove runtime dep on pbr.
sed -i s/REDHATNEUTRONCLIENTVERSION/%{version}/ neutronclient/version.py

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Install other needed files
# rhbz 888939#c7: bash-completion is not in RHEL
install -p -D -m 644 tools/neutron.bash_completion \
    %{buildroot}%{_sysconfdir}/profile.d/neutron.sh

# Remove unused files
rm -rf %{buildroot}%{python_sitelib}/neutronclient/tests

%files
%doc LICENSE
%doc README.rst
%{_bindir}/neutron
%{python_sitelib}/neutronclient
%{python_sitelib}/*.egg-info
%{_sysconfdir}/profile.d/neutron.sh

%changelog
* Tue Feb 25 2014 Jakub Ruzicka <jruzicka@redhat.com> 2.3.4-1
- Update to upstream 2.3.4

* Mon Jan 13 2014 Jakub Ruzicka <jruzicka@redhat.com> 2.3.3-1
- Update to upstream 2.3.3

* Fri Nov 01 2013 Jakub Ruzicka <jruzicka@redhat.com> - 2.3.1-2
- Don't obsolete python-quantumclient (#1025509)

* Tue Oct 08 2013 Jakub Ruzicka <jruzicka@redhat.com> - 2.3.1-1
- Update to upstream 2.3.1.

* Mon Sep 09 2013 Jakub Ruzicka <jruzicka@redhat.com> - 2.3.0-1
- Update to upstream 2.3.0.

* Wed Aug 28 2013 Jakub Ruzicka <jruzicka@redhat.com> - 2.2.6-2
- Remove all pbr deps in the patch instead of this spec file.

* Tue Aug 27 2013 Jakub Ruzicka <jruzicka@redhat.com> - 2.2.6-1
- Update to upstream 2.2.6.

* Tue Jul 23 2013 Jakub Ruzicka <jruzicka@redhat.com> - 1:2.2.4-1
- Initial package based on python-quantumclient.
- Removed runtime dependency on python-pbr.