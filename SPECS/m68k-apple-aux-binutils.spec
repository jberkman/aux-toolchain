%define _gnu %{nil}
%define _cross_target m68k-apple-aux
%define _build %{_build_arch}-%{_vendor}-%{_os}

%ifarch m68k
%define _host		%{_cross_target}
%define _prefix		/usr/local/gnu
%define _exec_prefix	%{_prefix}
%define _bindir		%{_exec_prefix}/bin
%define _sbindir	%{_exec_prefix}/sbin
%define _libexecdir	%{_exec_prefix}/libexec
%define _datadir	%{_prefix}/share
%define _sysconfdir	%{_prefix}/etc
%define _sharedstatedir	%{_prefix}/com
%define _localstatedir	%{_prefix}/var
%define _lib		lib
%define _libdir		%{_exec_prefix}/%{_lib}
%define _includedir	%{_prefix}/include
%define _oldincludedir	/usr/include
%define _infodir	%{_prefix}/info
%define _mandir		%{_prefix}/man
%define __strip		/usr/bin/%{_cross_target}-strip
%define __objdump	/usr/bin/%{_cross_target}-objdump
%define optflags	-O2 -D_POSIX_SOURCE
#%define posixcflags	-D_POSIX_SOURCE
#%define posixlibflags	-lposix
%else
%define _host %{_build}
#%define posixcflags %{nil}
#%define posixlibflags %{nil}
%endif

Summary: A GNU collection of binary utilities.
%ifarch m68k
Name: binutils
%else
Name: %{_cross_target}-binutils
%endif
Version: 2.14
Release: 1
Copyright: GPL
Group: Development/Tools
URL: https://www.gnu.org/software/binutils/
Source: https://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.bz2
Patch0: binutils-2.14-havesysconf.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Binutils is a collection of binary utilities, including ar (for
creating, modifying and extracting from archives), as (a family of GNU
assemblers), gprof (for displaying call graph profile data), ld (the
GNU linker), nm (for listing symbols from object files), objcopy (for
copying and translating object files), objdump (for displaying
information from object files), ranlib (for generating an index for
the contents of an archive), size (for listing the section sizes of an
object or archive file), strings (for listing printable strings from
files), strip (for discarding symbols), and addr2line (for converting
addresses to file and line).

%prep
%setup -q -n binutils-%{version}
%patch0 -p1 -b .havesysconf~

%build
# echo "_arch: %{_arch}"
# echo "_build_arch: %{_build_arch}"
# echo "_build_cpu: %{_build_cpu}"
# echo "_host_cpu: %{_host_cpu}"
# echo "_target_cpu: %{_target_cpu}"
# echo "_vendor: %{_vendor}"
%{__mkdir_p} build-%{_cross_target}
cd build-%{_cross_target}
# LIBS="${LIBS:-%posixlibflags}" ; export LIBS ; \
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ; \
../configure --host=%{_host} --build=%{_build} \
	--target=%{_cross_target} \
	--program-prefix=%{?_program_prefix} \
 	--prefix=%{_prefix} \
	--exec-prefix=%{_exec_prefix} \
	--bindir=%{_bindir} \
	--sbindir=%{_sbindir} \
	--sysconfdir=%{_sysconfdir} \
	--datadir=%{_datadir} \
	--includedir=%{_includedir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--localstatedir=%{_localstatedir} \
	--sharedstatedir=%{_sharedstatedir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
%ifnarch m68k
	--with-sysroot \
%endif
	--disable-nls
%{__make} %{_smp_mflags} tooldir=%{_prefix} all
echo ====================TESTING=========================
%{__make} -k check || :
echo ====================TESTING END=====================
cd ..

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_prefix}
cd build-%{_cross_target}
%makeinstall
%{__gzip} -q9f %{buildroot}%{_infodir}/*.info*

%ifnarch m68k
%{__rm} -f %{buildroot}%{_prefix}/%{_lib}/libiberty.a
%{__rm} -rf %{buildroot}%{_infodir}
%endif

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README
%{_prefix}/bin/*
%{_prefix}/%{_cross_target}/bin/*
%{_prefix}/%{_cross_target}/%{_lib}/ldscripts/*
%{_mandir}/man1/*
%ifarch m68k
%{_prefix}/include/*
%{_prefix}/%{_lib}/*
%{_infodir}/*info*
%else
%{_prefix}/%{_host}/%{_cross_target}/include/*
%{_prefix}/%{_host}/%{_cross_target}/%{_lib}/*
%endif

%changelog
* Mon Sep 06 2021 Jacob Berkman <jacob@87k.net> 2.14-1
- Build as cross-toolchain

* Mon Feb 24 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-9
- rebuilt

* Mon Feb 24 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-8
- don't strip binaries in %%install, so that there is non-empty
  debuginfo

* Mon Feb 24 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-7
- don't optimize .eh_frame during ld -r

* Thu Feb 13 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-6
- don't clear elf_link_hash_flags in the .symver patch
- only use TC_FORCE_RELOCATION in s390's TC_FORCE_RELOCATION_SUB_SAME
  (Alan Modra)

* Mon Feb 10 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-5
- fix the previous .symver change
- remove libbfd.so and libopcodes.so symlinks, so that other packages
  link statically, not dynamically against libbfd and libopcodes
  whose ABI is everything but stable

* Mon Feb 10 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-4
- do .symver x, x@FOO handling earlier
- support .file and .loc on s390*

* Mon Feb 10 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-3
- handle .symver x, x@FOO in ld such that relocs against x become
  dynamic relocations against x@FOO (#83325)
- two PPC64 TLS patches (Alan Modra)

* Sun Feb 09 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-2
- fix SEARCH_DIR on x86_64/s390x
- fix Alpha --relax
- create DT_RELA{,SZ,ENT} on s390 even if there is just .rela.plt
  and no .rela.dyn section
- support IA-32 on IA-64 (#83752)
- .eh_frame_hdr fix (Andreas Schwab)

* Thu Feb 06 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-1
- update to 2.13.90.0.18 + 20030121->20030206 CVS diff

* Tue Feb 04 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.16-8
- alpha TLS fixes
- use .debug_line directory table to make the section tiny bit smaller
- libtool fix from Jens Petersen

* Sun Feb 02 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.16-7
- sparc32 TLS

* Fri Jan 24 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.16-6
- s390{,x} TLS and two other mainframe patches

* Fri Jan 17 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.16-5
- fix IA-64 TLS IE in shared libs
- .{preinit,init,fini}_array compat hack from Alexandre Oliva

* Thu Jan 16 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.16-4
- IA-64 TLS fixes
- fix .plt sh_entsize on Alpha
- build with %%_smp_mflags

* Sat Nov 30 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.16-3
- fix strip on TLS binaries and libraries

* Fri Nov 29 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.16-2
- fix IA-64 ld bootstrap

* Thu Nov 28 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.16-1
- update to 2.13.90.0.16
- STT_TLS SHN_UNDEF fix

* Wed Nov 27 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.10-4
- pad .rodata.cstNN sections at the end if they aren't sized to multiple
  of sh_entsize
- temporary patch to make .eh_frame and .gcc_except_table sections
  readonly if possible (should be removed when AUTO_PLACE is implemented)
- fix .PPC.EMB.apuinfo section flags

* Wed Oct 23 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.10-3
- fix names and content of alpha non-alloced .rela.* sections (#76583)
- delete unpackaged files from the buildroot

* Tue Oct 15 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.10-2
- enable s390x resp. s390 emulation in linker too

* Mon Oct 14 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.10-1
- update to 2.13.90.0.10
- add a bi-arch patch for sparc/s390/x86_64
- add --enable-64-bit-bfd on sparc, s390 and ppc

* Thu Oct 10 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.4-3
- fix combreloc testcase

* Thu Oct 10 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.4-2
- fix orphan .rel and .rela section placement with -z combreloc (Alan Modra)
- skip incompatible linker scripts when searching for libraries

* Tue Oct  1 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.4-1
- update to 2.13.90.0.4
- x86-64 TLS support
- some IA-32 TLS fixes
- some backported patches from trunk
- include opcodes, ld, gas and bfd l10n too

* Thu Sep 19 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.2-3
- allow addends for IA-32 TLS @tpoff, @ntpoff and @dtpoff
- clear memory at *r_offset of dynamic relocs on PPC
- avoid ld crash if accessing non-local symbols through LE relocs
- new IA-32 TLS relocs, bugfixes and testcases
- use brl insn on IA-64 (Richard Henderson)
- fix R_IA64_PCREL21{M,F} handling (Richard Henderson)
- build in separate builddir, so that gasp tests don't fail
- include localization

* Thu Aug  8 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.2-2
- fix R_386_TPOFF32 addends (#70824)

* Sat Aug  3 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.2-1
- update to 2.13.90.0.2
  - fix ld TLS assertion failure (#70084)
  - fix readelf --debug-dump= handling to match man page and --help
    (#68997)
- fix _GLOBAL_OFFSET_TABLE gas handling (#70241)

* Wed Jul 24 2002 Jakub Jelinek <jakub@redhat.com> 2.12.90.0.15-1
- update to 2.12.90.0.15
- TLS .tbss fix
- don't use rpm %%configure macro, it is broken too often (#69366)

* Thu May 30 2002 Jakub Jelinek <jakub@redhat.com> 2.12.90.0.9-1
- update to 2.12.90.0.9
  - TLS support
- remove gasp.info from %%post/%%preun (#65400)

* Mon Apr 29 2002 Jakub Jelinek <jakub@redhat.com> 2.12.90.0.7-1
- update to 2.12.90.0.7
- run make check

* Mon Apr 29 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-12
- fix .hidden handling on SPARC (Richard Henderson)
- don't crash when linking -shared non-pic code with SHF_MERGE
- fix .eh_frame_hdr for DW_EH_PE_aligned
- correctly adjust DW_EH_PE_pcrel encoded personalities in CIEs

* Fri Apr  5 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-11
- don't emit dynamic R_SPARC_DISP* relocs against STV_HIDDEN symbols
  into shared libraries

* Thu Mar 21 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-10
- don't merge IA-64 unwind info sections together during ld -r

* Mon Mar 11 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-9
- fix DATA_SEGMENT_ALIGN on ia64/alpha/sparc/sparc64

* Fri Mar  8 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-8
- don't crash on SHN_UNDEF local dynsyms (Andrew MacLeod)

* Thu Mar  7 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-7
- fix bfd configury bug (Alan Modra)

* Tue Mar  5 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-6
- don't copy visibility when equating symbols
- fix alpha .text/.data with .previous directive bug

* Tue Mar  5 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-5
- fix SHF_MERGE crash with --gc-sections (#60369)
- C++ symbol versioning patch

* Fri Feb 22 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-4
- add DW_EH_PE_absptr -> DW_EH_PE_pcrel optimization for shared libs,
  if DW_EH_PE_absptr cannot be converted that way, don't build the
  .eh_frame_hdr search table

* Fri Feb 15 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-3
- fix ld -N broken by last patch

* Tue Feb 12 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-2
- trade one saved runtime page for data segment (=almost always not shared)
  for up to one page of disk space where possible

* Fri Feb  8 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-1
- update to 2.11.93.0.2
- use %%{ix86} instead of i386 for -z combreloc default (#59086)

* Thu Jan 31 2002 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-10
- don't create SHN_UNDEF STB_WEAK symbols unless there are any relocations
  against them

* Wed Jan 30 2002 Bill Nottingham <notting@redhat.com> 2.11.92.0.12-9.1
- rebuild (fix ia64 miscompilation)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 28 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-8
- two further .eh_frame patch fixes

* Wed Dec 19 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-7
- as ld is currently not able to shrink input sections to zero size
  during discard_info, build a fake minimal CIE in that case
- update elf-strtab patch to what was commited

* Mon Dec 17 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-6
- one more .eh_frame patch fix
- fix alpha .eh_frame handling
- optimize elf-strtab finalize

* Sat Dec 15 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-5
- yet another fix for the .eh_frame patch

* Fri Dec 14 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-4
- Alan Modra's patch to avoid crash if there is no dynobj

* Thu Dec 13 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-3
- H.J.'s patch to avoid crash if input files are not ELF
- don't crash if a SHF_MERGE for some reason could not be merged
- fix objcopy/strip to preserve SHF_MERGE sh_entsize
- optimize .eh_frame sections, add PT_GNU_EH_FRAME support
- support anonymous version tags in version script

* Tue Nov 27 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-2
- fix IA-64 SHF_MERGE handling

* Tue Nov 27 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-1
- update to 2.11.92.0.12
  - optimize .dynstr and .shstrtab sections (#55524)
  - fix ld.1 glitch (#55459)
- turn relocs against SHF_MERGE local symbols with zero addend
  into STT_SECTION + addend
- remove man pages for programs not included (nlmconv, windres, dlltool;
  #55456, #55461)
- add BuildRequires for texinfo

* Thu Oct 25 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.7-2
- duh, fix strings on bfd objects (#55084)

* Sat Oct 20 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.7-1
- update to 2.11.92.0.7
- remove .rel{,a}.dyn from output if it is empty

* Thu Oct 11 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.5-2
- fix strings patch
- use getc_unlocked in strings to speed it up by 50% on large files

* Wed Oct 10 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.5-1
- update to 2.11.92.0.5
  - binutils localization (#45148)
  - fix typo in REPORT_BUGS_TO (#54325)
- support files bigger than 2GB in strings (#54406)

* Wed Sep 26 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-12
- on IA-64, don't mix R_IA64_IPLTLSB relocs with non-PLT relocs in
  .rela.dyn section.

* Tue Sep 25 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-11
- add iplt support for IA-64 (Richard Henderson)
- switch to new section flags for SHF_MERGE and SHF_STRINGS, put
  in compatibility code
- "s" section flag for small data sections on IA-64 and Alpha
  (Richard Henderson)
- fix sparc64 .plt[32768+] handling
- don't emit .rela.stab on sparc

* Mon Sep 10 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-10
- fix SHF_MERGE on Sparc

* Fri Aug 31 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-9
- on Alpha, copy *r_offset to R_ALPHA_RELATIVE's r_addend

* Thu Aug 30 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-8
- on IA-64, put crtend{,S}.o's .IA_64.unwind section last in
  .IA_64.unwind output section (for compatibility with 7.1 eh)

* Fri Aug 24 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-7
- put RELATIVE relocs first, not last
- enable -z combreloc by default on IA-{32,64}, Alpha, Sparc*

* Thu Aug 23 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-6
- support for -z combreloc
- remove .dynamic patch, -z combreloc patch does this better
- set STT_FUNC default symbol sizes in .endp directive on IA-64

* Mon Jul 16 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-5
- fix last patch (H.J.Lu)

* Fri Jul 13 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-4
- fix placing of orphan sections

* Sat Jun 23 2001 Jakub Jelinek <jakub@redhat.com>
- fix SHF_MERGE support on Alpha

* Fri Jun  8 2001 Jakub Jelinek <jakub@redhat.com>
- 2.11.90.0.8
  - some SHF_MERGE suport fixes
- don't build with tooldir /usrusr instead of /usr (#40937)
- reserve few .dynamic entries for prelinking

* Mon Apr 16 2001 Jakub Jelinek <jakub@redhat.com>
- 2.11.90.0.5
  - SHF_MERGE support

* Tue Apr  3 2001 Jakub Jelinek <jakub@redhat.com>
- 2.11.90.0.4
  - fix uleb128 support, so that CVS gcc bootstraps
  - some ia64 fixes

* Mon Mar 19 2001 Jakub Jelinek <jakub@redhat.com>
- add -Bgroup support from Ulrich Drepper

* Fri Mar  9 2001 Jakub Jelinek <jakub@redhat.com>
- hack - add elf_i386_glibc21 emulation

* Fri Feb 16 2001 Jakub Jelinek <jakub@redhat.com>
- 2.10.91.0.2

* Fri Feb  9 2001 Jakub Jelinek <jakub@redhat.com>
- 2.10.1.0.7
- remove ExcludeArch ia64
- back out the -oformat, -omagic and -output change for now

* Fri Dec 15 2000 Jakub Jelinek <jakub@redhat.com>
- Prereq /sbin/install-info

* Tue Nov 21 2000 Jakub Jelinek <jakub@redhat.com>
- 2.10.1.0.2

* Tue Nov 21 2000 Jakub Jelinek <jakub@redhat.com>
- add one more alpha patch

* Wed Nov 15 2000 Jakub Jelinek <jakub@redhat.com>
- fix alpha visibility as problem
- add support for Ultra-III

* Fri Sep 15 2000 Jakub Jelinek <jakub@redhat.com>
- and one more alpha patch

* Fri Sep 15 2000 Jakub Jelinek <jakub@redhat.com>
- two sparc patches

* Mon Jul 24 2000 Jakub Jelinek <jakub@redhat.com>
- 2.10.0.18

* Mon Jul 10 2000 Jakub Jelinek <jakub@redhat.com>
- 2.10.0.12

* Mon Jun 26 2000 Jakub Jelinek <jakub@redhat.com>
- 2.10.0.9

* Thu Jun 15 2000 Jakub Jelinek <jakub@redhat.com>
- fix ld -r

* Mon Jun  5 2000 Jakub Jelinek <jakub@redhat.com>
- 2.9.5.0.46
- use _mandir/_infodir/_lib

* Mon May  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.41

* Wed Apr 12 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.34

* Wed Mar 22 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.31

* Fri Feb 04 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- apply kingdon's patch from #5031

* Wed Jan 19 2000 Jeff Johnson <jbj@redhat.com>
- Permit package to be built with a prefix other than /usr.

* Thu Jan 13 2000 Cristian Gafton <gafton@redhat.com>
- add pacth from hjl to fix the versioning problems in ld

* Tue Jan 11 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add sparc patches from Jakub Jelinek <jakub@redhat.com>
- Add URL:

* Tue Dec 14 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.22

* Wed Nov 24 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.19

* Sun Oct 24 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.16

* Mon Sep 06 1999 Jakub Jelinek <jj@ultra.linux.cz>
- make shared non-pic libraries work on sparc with glibc 2.1.

* Fri Aug 27 1999 Jim Kingdon
- No source/spec changes, just rebuilding with egcs-1.1.2-18 because
  the older egcs was miscompling gprof.

* Mon Apr 26 1999 Cristian Gafton <gafton@redhat.com>
- back out very *stupid* sparc patch done by HJLu. People, keep out of
  things you don't understand.
- add alpha relax patch from rth

* Mon Apr 05 1999 Cristian Gafton <gafton@redhat.com>
- version  2.9.1.0.23
- patch to make texinfo documentation compile
- auto rebuild in the new build environment (release 2)

* Tue Feb 23 1999 Cristian Gafton <gafton@redhat.com>
- updated to 2.9.1.0.21
- merged with UltraPenguin

* Mon Jan 04 1999 Cristian Gafton <gafton@redhat.com>
- added ARM patch from philb
- version 2.9.1.0.19a
- added a patch to allow arm* arch to be identified as an ARM

* Thu Oct 01 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.9.1.0.14.

* Sat Sep 19 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.9.1.0.13.

* Wed Sep 09 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.9.1.0.12

* Thu Jul  2 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.9.1.0.7.

* Wed Jun 03 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.9.1.0.6.

* Tue Jun 02 1998 Erik Troan <ewt@redhat.com>
- added patch from rth to get right offsets for sections in relocateable
  objects on sparc32

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue May 05 1998 Cristian Gafton <gafton@redhat.com>
- version 2.9.1.0.4 is out; even more, it is public !

* Tue May 05 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.9.1.0.3.

* Mon Apr 20 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.9.0.3

* Tue Apr 14 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 2.9.0.2

* Sun Apr 05 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.8.1.0.29 (HJ warned me that this thing is a moving target...
  :-)
- "fixed" the damn make install command so that all tools get installed

* Thu Apr 02 1998 Cristian Gafton <gafton@redhat.com>
- upgraded again to 2.8.1.0.28 (at least on alpha now egcs will compile)
- added info packages handling

* Tue Mar 10 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 2.8.1.0.23

* Mon Mar 02 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.8.1.0.15 (required to compile the newer glibc)
- all patches are obsoleted now

* Wed Oct 22 1997 Erik Troan <ewt@redhat.com>
- added 2.8.1.0.1 patch from hj
- added patch for alpha palcode form rth
