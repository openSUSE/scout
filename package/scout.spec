#
# spec file for package scout (Version 0.1.0)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           scout
Version:        0.1.0
Release:        1
Url:            http://en.opensuse.org/Scout
License:        X11/MIT
Group:          System/Packages
Summary:        Package Scout
Source:         %{name}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python rpm-python
Requires:       python

%if 0%{?suse_version}
BuildRequires:  python-xml
Requires:       python-xml
%endif
%if 0%{?suse_version} > 1030
BuildRequires:  python-satsolver > 0.10.2
Requires:       python-satsolver > 0.10.2
%endif

%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
%define py_sitedir %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif

# workaround conflicting readline packages
%if 0%{?suse_version} <= 1020
BuildRequires:  readline
%endif

%description
Package Scout for indexing various properties of packages.



%define cnfrepo none
%if 0%{?suse_version} > 1030
%define cnfrepo zypp
%endif
%if 0%{?suse_version} <= 1030 && 0%{?suse_version} > 1020
%define cnfrepo suse103
%endif
%if 0%{?suse_version} <= 1020 && 0%{?suse_version} > 1010
%define cnfrepo suse102
%endif
%if 0%{?suse_version} <= 1010 && 0%{?suse_version} > 1000
%define cnfrepo suse101
%endif
%if 0%{?sles_version} == 10
%define cnfrepo sle10
%endif

%if %{cnfrepo} != none

%package -n command-not-found
Version:        0.1.0
Release:        2
License:        X11/MIT
Group:          System/Packages
Summary:        Command Not Found extension for shell
Requires:       python rpm-python scout
# Requires:       bash(CommandNotFound)
%if %{cnfrepo} != zypp
Requires:       scout-bin-%{cnfrepo}
%endif

%description -n command-not-found
The "command not found" message is not very helpful. If e.g. the unzip
command is not found but it's available in a package, it would be very
interesting if the system could tell that the command is currently not
available, but installing a package would provide it.



%endif

%prep
%setup -q -n %{name}

%build
# compile scripts
python -mcompileall .

%install
# --- scout ---
# install python scripts
mkdir -p $RPM_BUILD_ROOT%{py_sitedir}/%{name}
shopt -s extglob
cp -a scout/!(foo).py{,c} $RPM_BUILD_ROOT%{py_sitedir}/%{name}
# install data files
install -D -m 0644 repos.conf $RPM_BUILD_ROOT%{_datadir}/%{name}/repos.conf
# install scout binary
install -D -m 0755 scout-cmd.py $RPM_BUILD_ROOT%{_bindir}/%{name}
# install bash completion
install -D -m 0644 scout-bash-completion $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/scout.sh
# install manpage
install -D -m 0644 doc/scout.1 $RPM_BUILD_ROOT%{_mandir}/man1/scout.1

%if %{cnfrepo} != none
# --- command-not-found ---
install -D -m 0755 handlers/bin/command-not-found $RPM_BUILD_ROOT%{_bindir}/command-not-found
for shell in bash zsh; do
    install -D -m 644 handlers/bin/command_not_found_${shell} $RPM_BUILD_ROOT%{_sysconfdir}/${shell}_command_not_found
    sed -i 's:__REPO__:%{cnfrepo}:' $RPM_BUILD_ROOT%{_sysconfdir}/${shell}_command_not_found
done

%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS LICENSE README TODO doc/scout.html doc/scout.pdf
%{_bindir}/%{name}*
%{py_sitedir}/%{name}
%{_datadir}/%{name}
%{_sysconfdir}/bash_completion.d/*
%{_mandir}/man1/*

%if %{cnfrepo} != none

%files -n command-not-found
%defattr(-,root,root)
%doc handlers/bin/README
%{_bindir}/command-not-found
%{_sysconfdir}/*_command_not_found

%endif

%changelog
