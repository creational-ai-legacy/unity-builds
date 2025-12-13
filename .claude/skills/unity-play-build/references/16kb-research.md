# Android 16KB Page Size Research - Complete Reference Guide

## Executive Summary

Starting **November 1st, 2025**, Google Play Store requires all new apps and updates targeting Android 15+ devices to support 16KB page sizes. This affects Unity exports and other native code applications that must rebuild shared libraries (.so files) with proper 16KB ELF alignment.

## Official Requirements & Timeline

### Google Play Store Mandate
- **Effective Date**: November 1st, 2025
- **Scope**: All new apps and updates to existing apps submitted to Google Play targeting Android 15+ devices
- **Requirement**: Must support 16KB page sizes for proper functionality

**Source**: [Android Developers - Support 16 KB page sizes](https://developer.android.com/guide/practices/page-sizes)

### Performance Benefits (Verified by Google)
- **App Launch Times**: 3.16% improvement on average (range: 3-30% for various apps)
- **Battery Usage**: 4.56% reduction in power draw during app launch (4.5% average gain)
- **Camera Launch**: 4.48% faster hot starts, 6.60% faster cold starts
- **System Boot**: ~8% faster boot times (approximately 950 milliseconds improvement)

**Source**: [Android Developers Blog - Prepare your apps for Google Play's 16 KB page size compatibility requirement](https://android-developers.googleblog.com/2025/05/prepare-play-apps-for-devices-with-16kb-page-size.html)

## Technical Requirements

### Native Code Applications
Apps using native C/C++ code must ensure:
1. **ELF Segment Alignment**: Shared libraries (.so files) must have ELF segments aligned to 16KB boundaries
2. **Recompilation Required**: All prebuilt shared libraries must be recompiled with 16KB alignment
3. **NDK Requirements**: Android NDK r28+ compiles with 16KB alignment by default

### Compatibility by App Type
- ✅ **Java/Kotlin Only**: Apps with no native code already support 16KB devices
- ⚠️ **Third-party Libraries**: Apps using libraries/SDKs with native code may need updates
- 🔧 **Native Code Apps**: Must recompile with recent toolchain supporting 16KB alignment

## Game Engine Support Status

### Unity Support Matrix

#### Unity 6.0 LTS (6000.1.0b5+) - ✅ **FULL SUPPORT**
- ✅ **Native 16KB Support**: Built-in support starting from Unity 6000.1.0b5+
- ✅ **Automatic ELF Alignment**: Unity Editor handles 16KB alignment automatically
- ✅ **Build Warnings**: Editor displays warnings for 4KB-aligned .so files during build
- ✅ **Dual Compatibility**: Same executable supports both 4KB and 16KB page size devices
- ✅ **NDK Integration**: Works with NDK r28+ which compiles 16KB-aligned by default
- ⚠️ **Third-party Plugin Dependency**: Still requires plugin creators to provide 16KB-compatible libraries

#### Unity 2022.3.x LTS - ⚠️ **LIMITED SUPPORT**
- ⚠️ **Claims Support**: Unity documentation states "Unity already supports 16KB page sizes"
- 🔧 **Export Issues**: Android Studio exports may generate libraries with incorrect alignment
- 🔧 **Manual Fix Required**: Need to fix ELF headers post-export (our solution addresses this)
- 🔧 **Third-party Plugin Issues**: Many plugins (IronSource, LofeltHaptics) ship with 4KB alignment
- 🔧 **NDK Version Issues**: Ships with older NDK versions that default to 4KB alignment

#### Migration Recommendation
**For Production Apps**: Upgrade to Unity 6.0 LTS (6000.1.0b5+) eliminates the need for manual ELF fixes and provides proper 16KB support out of the box.

**Migration Timeline Strategy**:
1. **Immediate (Unity 2022.3.x)**: Use our ELF alignment fix for Google Play compliance
2. **Short-term**: Upgrade to Unity 6.0 LTS for native 16KB support  
3. **Long-term**: Update to modern plugin ecosystem (e.g., IronSource LevelPlay 8.10) for full compatibility

### Other Engines
- ✅ **React Native**: Compatible versions available
- ✅ **Flutter**: Compatible versions available  
- 🚧 **Unreal Engine**: Support coming soon

**Source**: [Android Developers Blog - Get your apps ready for 16 KB page size devices](https://android-developers.googleblog.com/2024/12/get-your-apps-ready-for-16-kb-page-size-devices.html)

## Technical Implementation Details

### Android Gradle Plugin (AGP) Support
- **Minimum Version**: AGP 8.5.1+ automatically enables 16KB alignment for uncompressed shared libraries
- **Automatic Handling**: Newer AGP versions handle alignment during packaging
- **Legacy Projects**: Older AGP versions require manual ELF header modification

### ELF Alignment Technical Details
- **Current Standard**: Most libraries use 4KB (0x1000) alignment  
- **New Requirement**: Must use 16KB (0x4000) alignment for LOAD segments
- **Detection Method**: Check ELF headers using tools like `readelf` or `objdump`
- **Fix Method**: Modify ELF program headers to change p_align values

### Testing & Validation
- **Android 15 Emulator**: Use 16KB system images for testing
- **Developer Options**: Available on supported Pixel devices
- **Samsung Remote Test Lab**: Provides 16KB testing environment
- **Android Studio Lint**: Highlights non-16KB aligned native libraries

## Unity-Specific Challenges

### Known Issues with Unity Exports
1. **Hardcoded NDK Paths**: Unity exports reference old NDK versions
2. **Incorrect ELF Alignment**: Generated .so files may have 4KB instead of 16KB alignment
3. **Third-party Plugin Issues**: Plugins like LofeltHaptics, IronSource may not be 16KB aligned
4. **Build System Conflicts**: Unity's build process can override AGP alignment settings

### Common Problematic Libraries in Unity
- `liblofelt_sdk.so` - From LofeltHaptics.aar (haptic feedback)
- `libnms.so` - From Unity/IronSource dependencies  
- `libtobEmbedPagEncrypt.so` - From Unity/advertising dependencies

## Our Solution Approach

### Why Post-Export ELF Fixing is Necessary
1. **Unity Export Limitations**: Unity 2022.3.x doesn't generate 16KB aligned libraries
2. **Third-party Plugin Issues**: Many Unity plugins ship with 4KB aligned libraries
3. **Build Process Timing**: AGP alignment may not catch all cases in Unity exports

### Technical Solution Overview
- **Direct ELF Modification**: Modify program headers after library stripping
- **Python Script Implementation**: Robust handling of both 32-bit and 64-bit ELF files
- **Gradle Integration**: Automatic execution during Android Studio build process
- **Backup Creation**: Safe modification with automatic backup generation

## Industry Impact & Adoption

### Developer Community Response
- **React Native**: [Issue #45054](https://github.com/facebook/react-native/issues/45054) tracks 16KB support
- **Medium Articles**: Multiple developer blogs covering preparation strategies
- **StackOverflow**: Growing number of questions about 16KB compliance

### Market Implications
- **Mandatory Compliance**: Apps failing to support 16KB may be rejected from Google Play
- **Performance Competitive Advantage**: Early adopters benefit from improved performance metrics
- **Development Timeline Impact**: Projects must allocate time for testing and fixing alignment issues

## References & Additional Resources

### Official Google Documentation
1. [Support 16 KB page sizes | Android Developers](https://developer.android.com/guide/practices/page-sizes)
2. [Android Developers Blog: Prepare your apps for Google Play's 16 KB page size compatibility requirement](https://android-developers.googleblog.com/2025/05/prepare-play-apps-for-devices-with-16kb-page-size.html)
3. [Android Developers Blog: Get your apps ready for 16 KB page size devices](https://android-developers.googleblog.com/2024/12/get-your-apps-ready-for-16-kb-page-size-devices.html)
4. [Android Developers Blog: Adding 16 KB Page Size to Android](https://android-developers.googleblog.com/2024/08/adding-16-kb-page-size-to-android.html)
5. [16 KB page size | Android Open Source Project](https://source.android.com/docs/core/architecture/16kb-page-size/16kb)

### Unity Official Documentation
6. [Unity 6.0 Manual: Android requirements and compatibility](https://docs.unity3d.com/6000.1/Documentation/Manual/android-requirements-and-compatibility.html)
7. [Unity Roadmap: Support for 16 KB page sizes](https://unity.com/roadmap/2712-support-for-16-kb-page-sizes)

### Technical Implementation Resources
- [Android Developers Blog: Transition to using 16 KB page sizes for Android apps and games using Android Studio](https://android-developers.googleblog.com/2025/07/transition-to-16-kb-page-sizes-android-apps-games-android-studio.html)
- [9to5Google: Google requiring Android apps support 16 KB memory page size](https://9to5google.com/2025/05/08/android-memory-page-size/)

### Community Resources & Discussions
- [Medium: Android 15+ Is Raising the Bar: Mandatory 16KB Memory Page Size](https://devharshmittal.medium.com/android-15-is-raising-the-bar-mandatory-16kb-memory-page-size-what-developers-need-to-know-4dd81ec58f67)
- [Medium: Prepare Your App: 16KB Page Size Becomes Mandatory for Android 15+](https://medium.com/@maydin/prepare-your-app-16kb-page-size-becomes-mandatory-for-android-15-1d0e717a808c)

## Conclusion

The 16KB page size requirement represents a significant shift in Android development practices. While Google provides tooling support through newer NDK and AGP versions, Unity developers face unique challenges requiring post-export ELF modification. Our solution addresses these Unity-specific issues while ensuring Google Play Store compliance and performance benefits.

**Key Takeaway**: This is not optional - all apps with native code must be 16KB compliant by November 1st, 2025, or risk rejection from Google Play Store.

---
*Document compiled from official Google sources and industry research - Last updated: January 2025*
