%{?_javapackages_macros:%_javapackages_macros}

%bcond_with bootstrap

Name:           antlr4
Version:        4.5.2
Release:        2
Summary:        Java parser generator
Group:		Development/Java
License:        BSD
URL:            http://www.antlr.org/
BuildArch:      noarch

Source0:        https://github.com/antlr/antlr4/archive/%{name}-%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Prebuild binaries, used for bootstrapping only
Source100:	http://download-ib01.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/x86_64/os/Packages/a/antlr4-4.5.2-8.fc31.noarch.rpm
source101:	https://download-ib01.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/x86_64/os/Packages/a/antlr4-runtime-4.5.2-8.fc31.noarch.rpm
Source102:	https://download-ib01.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/x86_64/os/Packages/a/antlr4-maven-plugin-4.5.2-8.fc31.noarch.rpm

BuildRequires:  maven-local
BuildRequires:  mvn(org.abego.treelayout:org.abego.treelayout.core)
BuildRequires:  mvn(org.antlr:antlr3-maven-plugin)
BuildRequires:  mvn(org.antlr:antlr-runtime)
BuildRequires:  mvn(org.antlr:ST4)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-project)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-compiler-api)
BuildRequires:  mvn(org.sonatype.oss:oss-parent:pom:)
BuildRequires:  mvn(org.sonatype.plexus:plexus-build-api)

%if %{without bootstrap}
BuildRequires:  mvn(org.antlr:antlr4-maven-plugin)
%endif

%description
ANTLR (ANother Tool for Language Recognition) is a powerful parser
generator for reading, processing, executing, or translating
structured text or binary files.  It's widely used to build languages,
tools, and frameworks. From a grammar, ANTLR generates a parser that
can build and walk parse trees.

%package runtime
Summary:        ANTLR runtime

%description runtime
This package provides runtime library used by parsers generated by
ANTLR.

%package maven-plugin
Summary:        ANTLR plugin for Apache Maven

%description maven-plugin
This package provides plugin for Apache Maven which can be used to
generate ANTLR parsers during build.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package contains %{summary}.

%prep
%setup -q
find -name \*.jar -delete

# Missing test deps: org.seleniumhq.selenium:selenium-java
%pom_disable_module runtime-testsuite
%pom_disable_module tool-testsuite

# Don't bundle dependencies
%pom_remove_plugin :maven-shade-plugin tool

%mvn_package :%{name}-master %{name}-runtime

%if %{with bootstrap}
for rpm in %{SOURCE100} %{SOURCE101} %{SOURCE102}; do rpm2cpio $rpm | cpio -id; done
sed -i "s,<path>,&$PWD," usr/share/maven-metadata/*
%mvn_config resolverSettings/metadataRepositories/repository $PWD/usr/share/maven-metadata
%endif

%build
%mvn_build -s -f

%install
%mvn_install

%jpackage_script org.antlr.v4.Tool "" "" antlr4/antlr4:antlr3-runtime:antlr4/antlr4-runtime:stringtemplate4:treelayout %{name} true

%files -f .mfiles-antlr4
%{_bindir}/%{name}
%doc tool/MIGRATION.txt

%files runtime -f .mfiles-antlr4-runtime
%doc CHANGES.txt README.md
%doc LICENSE.txt

%files maven-plugin -f .mfiles-antlr4-maven-plugin

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Mon Mar 30 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.5-2
- Post-review cleanup

* Thu Mar 26 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.5-1
- Initial packaging
