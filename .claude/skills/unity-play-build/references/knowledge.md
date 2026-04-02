# Android Studio Unity Export - Complete Fix Guide

## Quick Reference
- **Total Fixes**: 16 comprehensive solutions
- **Key Files Modified**: 8+ files across build.gradle, AndroidManifest.xml, and properties
- **Time to Fix**: ~45-60 minutes (including downloads)
- **Target API**: 35 (Android 15) - Google Play compliant
- **Unity Version**: 2022.3.62f1+ (applies to all Unity Android exports)

## Table of Contents

### 📋 Setup & Reference
- [Project Requirements](#project-requirements)
- [Build Commands Reference](#build-commands-reference)

### 🔧 Core Fixes
1. **[Project Setup & Requirements](#1-project-setup--requirements)**
   - [API Level & Namespace Configuration](#api-level--namespace-configuration) - Unity namespace missing for API 35
   - [NDK Installation & Configuration](#ndk-installation--configuration) - Unity hardcoded NDK paths
   - [Android Gradle Plugin & Build Tools Update](#android-gradle-plugin--build-tools-update) - Outdated AGP version

2. **[Java & Build Configuration](#2-java--build-configuration)**
   - [Java Version Configuration](#java-version-configuration) - AGP 8.11.1+ requires Java 17+
   - [BuildConfig Management](#buildconfig-management) - Multiple BuildConfig conflicts

3. **[Dependencies & Libraries](#3-dependencies--libraries)**
   - [Dependency Version Conflicts Resolution](#dependency-version-conflicts-resolution) - JAR vs Gradle conflicts
   - [Google Play Core Library Migration](#google-play-core-library-migration) - Legacy library conflicts
   - [IronSource Ad Quality SDK Update](#ironsource-ad-quality-sdk-update) - Google Play blocking v7.18.1
   - [Install Referrer Library Version Mismatch](#install-referrer-library-version-mismatch) - Runtime crash from old AAR

4. **[Android Manifest & Permissions](#4-android-manifest--permissions)**
   - [AD_ID Permission for Android 13+](#ad_id-permission-for-android-13) - Required for advertising
   - [Unity Activity Configuration](#unity-activity-configuration) - Missing Unity activity
   - [Firebase Manifest Conflicts](#firebase-manifest-conflicts) - Service exported conflicts

5. **[Build Optimization & Packaging](#5-build-optimization--packaging)**
   - [Resource Pattern Fix (APK/AAB Builds)](#resource-pattern-fix-apkaab-builds) - Malformed noCompress patterns
   - [MultiDex Configuration](#multidex-configuration) - ClassNotFoundException crashes
   - [Minification & ProGuard Rules](#minification--proguard-rules) - Plugin class stripping

6. **[Google Play Compliance](#6-google-play-compliance)**
   - [16KB Page Size Alignment Fix](#16kb-page-size-alignment-fix) - Nov 2025 requirement
   - [Signing Configuration](#signing-configuration) - Keystore setup

### 🔍 Support & Reference
- [Build Output Locations](#build-output-locations)
- [Troubleshooting](#troubleshooting)
- [Google Play Submission Checklist](#google-play-submission-checklist)
- [Future Unity Exports](#future-unity-exports)

---

## Project Requirements

### SDK Components Verification
| Component | Required Version | Installation Path |
|-----------|-----------------|-------------------|
| Platform SDK | API 35 | `/Users/[username]/Library/Android/sdk/platforms/android-35` |
| Build Tools | 35.0.0 | `/Users/[username]/Library/Android/sdk/build-tools/35.0.0` |
| NDK | 27.0.12077973 | `/Users/[username]/Library/Android/sdk/ndk/27.0.12077973` |

### System Requirements
- **Java**: 17+ (Android Studio bundled Java 21 recommended)
- **Unity**: 2022.3.62f1+ with IL2CPP backend
- **Android Studio**: Latest with AGP 8.11.1+

## Build Commands Reference
```bash
# Clean build
./gradlew clean

# Build APK
./gradlew assembleRelease

# Build AAB (Android App Bundle)  
./gradlew bundleRelease

# Debug with verbose output
./gradlew --info build

# Check dependencies for conflicts
./gradlew dependencies --configuration releaseRuntimeClasspath

# Accept SDK licenses if needed
./gradlew --stop  # Stop daemon first
/path/to/Android/sdk/cmdline-tools/latest/bin/sdkmanager --licenses
```

---

## Core Fixes (In Application Order)

## 1. Project Setup & Requirements

### 1.1 API Level & Namespace Configuration
**Problem**: Unity exports lack required namespace and package declarations for API 35

**Error Message**: 
```
Failed to calculate the value of property 'namespace'. Package Name not found in AndroidManifest.xml
```

**Files Fixed**:
- `unityLibrary/build.gradle`
- `unityLibrary/src/main/AndroidManifest.xml`

**Solution**:
```gradle
// unityLibrary/build.gradle
android {
    namespace 'com.your.package.name'  // Add this line
    compileSdkVersion 35
    // ... rest of config
}
```

```xml
<!-- AndroidManifest.xml -->
<manifest xmlns:android="http://schemas.android.com/apk/res/android" 
    package="com.your.package.name"  <!-- Add package attribute -->
    android:installLocation="preferExternal">
```

**Why This Happens**: Unity 2022.3 doesn't automatically add namespace/package declarations when targeting API 35, requiring manual addition for Google Play compliance.

### 1.2 NDK Installation & Configuration
**Problem**: Unity hardcodes NDK paths causing build failures

**Error Message**:
```
NDK not configured. Download it with SDK manager.
```

**Actions Required**:
1. **Install NDK via Android Studio**:
   - SDK Manager → SDK Tools → NDK (Side by side) → Version 27.0.12077973

2. **Update local.properties**:
```properties
sdk.dir=/Users/[username]/Library/Android/sdk
ndk.dir=/Users/[username]/Library/Android/sdk/ndk/27.0.12077973
```

3. **Remove hardcoded NDK paths** from all build.gradle files:
```gradle
// REMOVE these lines if present:
// ndkPath "/Applications/Unity/Hub/Editor/2022.3.62f1/PlaybackEngines/AndroidPlayer/NDK"
```

**Why Unity Version Matters**: Unity 2022.3 LTS IL2CPP specifically requires NDK 27.0.12077973. Stick with LTS versions for stability.

### 1.3 Android Gradle Plugin & Build Tools Update
**Problem**: Outdated AGP version incompatible with API 35

**Solution**: 
1. Use Android Studio's Upgrade Assistant (recommended)
2. Manually update to AGP 8.11.1+ 
3. Remove explicit buildToolsVersion (uses default 35.0.0):

```gradle
android {
    compileSdkVersion 35
    // buildToolsVersion '34.0.0' - REMOVE this line
}
```

**Benefits**: Enables modern Android 15 features, better namespace handling, and Google Play Store compliance.

## 2. Java & Build Configuration

### 2.1 Java Version Configuration
**Problem**: AGP 8.11.1+ requires Java 17+ but systems often default to older versions

**Error Message**:
```
Android Gradle plugin requires Java 17 to run. You are currently using Java 11.
Your current JDK is located in /Library/Java/JavaVirtualMachines/microsoft-11.jdk/Contents/Home
```

**File Fixed**: `gradle.properties`

**Solution (Recommended)** - Use Android Studio's bundled Java 21:
```properties
# Add to gradle.properties
org.gradle.java.home=/Applications/Android Studio.app/Contents/jbr/Contents/Home
```

**Alternative Solutions**:

**Option A** - Install Java 17 manually:
```bash
brew install openjdk@17
# Then set in gradle.properties:
org.gradle.java.home=/opt/homebrew/Cellar/openjdk@17/[version]/libexec/openjdk.jdk/Contents/Home
```

**Option B** - For backward compatibility (Java 8/11 projects):
```gradle
// In both launcher/build.gradle and unityLibrary/build.gradle
compileOptions {
    sourceCompatibility JavaVersion.VERSION_1_8  // or VERSION_11
    targetCompatibility JavaVersion.VERSION_1_8  // or VERSION_11
}
```

**AGP vs Java Compatibility**:
| Android Gradle Plugin | Minimum Java | Recommended |
|----------------------|--------------|-------------|
| 8.0.x - 8.2.x        | Java 11     | Java 17     |
| 8.3.x - 8.11.x       | Java 17     | Java 17     |
| 8.12.x+              | Java 17     | Java 21     |

### 2.2 BuildConfig Management
**Problem**: Multiple modules generating conflicting BuildConfig classes

**Error Messages**:
```
The option setting 'android.defaults.buildfeatures.buildconfig=true' is deprecated
Type com.your.package.BuildConfig is defined multiple times
```

**Files Fixed**: Various build.gradle files

**Solution**:

1. **Enable in main launcher module** (`launcher/build.gradle`):
```gradle
android {
    buildFeatures {
        buildConfig = true
    }
}
```

2. **Disable in library modules** (`unityLibrary/build.gradle`, `IronSource.androidlib/build.gradle`):
```gradle
android {
    buildFeatures {
        buildConfig = false  // Prevents conflicts
    }
}
```

**Why This Happens**: Unity exports often have multiple modules that all try to generate BuildConfig classes with the same package name, causing R8 minification failures.

## 3. Dependencies & Libraries

### 3.1 Dependency Version Conflicts Resolution
**Problem**: Unity includes old JAR files conflicting with newer Gradle dependencies

**Error Messages**:
```
Duplicate class kotlin.ArrayIntrinsicsKt found in modules kotlin-stdlib-1.9.22.jar and org.jetbrains.kotlin.kotlin-stdlib-1.5.31.jar
Duplicate class okhttp3.Address found in modules com.squareup.okhttp3.okhttp-4.2.2.jar and okhttp-4.10.0.jar
Duplicate class org.intellij.lang.annotations.Flow found in modules annotations-23.0.0.jar and org.jetbrains.annotations-13.0.jar
```

**Root Cause**: Unity exports include physical JAR files in `unityLibrary/libs/` that conflict with newer versions resolved by Android Gradle Plugin dependencies.

**File Fixed**: `unityLibrary/build.gradle`

**Solution**:

1. **Exclude conflicting JAR files from libs folder**:
```gradle
dependencies {
    implementation fileTree(dir: 'libs', include: ['*.jar'], exclude: [
        'org.jetbrains.kotlin.kotlin-stdlib-*.jar',
        'org.jetbrains.kotlinx.kotlinx-coroutines-*.jar',
        'com.squareup.okhttp3.okhttp-*.jar',
        'com.squareup.okio.okio-*.jar',
        'org.jetbrains.annotations-*.jar'
    ])
    // ... rest of dependencies
}
```

2. **Force consistent dependency versions**:
```gradle
android {
    configurations.all {
        resolutionStrategy {
            // Force consistent Kotlin version to resolve duplicate class conflicts
            force 'org.jetbrains.kotlin:kotlin-stdlib:1.9.22'
            force 'org.jetbrains.kotlin:kotlin-stdlib-jdk7:1.9.22'
            force 'org.jetbrains.kotlin:kotlin-stdlib-jdk8:1.9.22'
            force 'org.jetbrains.kotlin:kotlin-stdlib-common:1.9.22'
        }
    }
}
```

**APK vs AAB Impact**:
- **APK builds**: More tolerant of conflicts (warnings only)
- **AAB builds**: Strict validation fails completely on duplicate classes

### 3.2 Google Play Core Library Migration
**Problem**: Unity exports use deprecated monolithic Google Play Core library conflicting with newer split libraries

**Error Message**:
```
Duplicate class com.google.android.play.core found in modules
```

**File Fixed**: `unityLibrary/build.gradle`

**Solution**:

1. **Comment out old monolithic library**:
```gradle
// implementation 'com.google.android.play:core:1.10.2'  // Old monolithic version - REMOVE
```

2. **Use newer split libraries**:
```gradle
implementation 'com.google.android.play:core-common:2.0.4'
implementation 'com.google.android.play:review:2.0.0'
```

3. **Force newer versions in resolution strategy**:
```gradle
android {
    configurations.all {
        resolutionStrategy {
            // Force newer Play Core split libraries
            force 'com.google.android.play:core-common:2.0.4'
            force 'com.google.android.play:review:2.0.0'
        }
    }
}
```

**Why This Migration Matters**: Google split the Play Core library for better modularity. Unity exports often include the old monolithic version that conflicts with newer dependencies.

### 3.3 IronSource Ad Quality SDK Update
**Problem**: Google Play blocks version 7.18.1 due to critical stability issues

**Error Message from Google Play Console**:
```
Your app uses an SDK version with a critical note from Ad Quality SDK
The developer of Ad Quality SDK (com.ironsource:adqualitysdk) has added a note to version 7.18.1:

We have identified an issue that might impact the stability of this version. Please integrate version 7.19.2 and above

To continue releasing new versions of your app, upgrade to a newer SDK version.
```

**File Fixed**: `unityLibrary/build.gradle`

**Solution**:
```gradle
// Update from problematic version
implementation 'com.ironsource:adqualitysdk:7.19.2' // Fixed version - was 7.18.1
```

**How to Identify**:
```bash
grep -r "adqualitysdk" unityLibrary/build.gradle
# Look for version 7.18.1
```

**Impact**: 
- **Critical** - Blocks ALL Google Play submissions
- **Timeline** - Must be resolved before any production uploads
- **Affects** - All Unity projects using IronSource mediation

**Related SDKs to Monitor**:
- `com.ironsource.sdk:mediationsdk`
- `com.ironsource.adapters:*` (all adapter SDKs)
- `com.ironsource:adqualitysdk` (this specific issue)

### 3.4 Unity Mediation SDK Namespace Conflicts (Unity 2022.3.62f1+)
**Problem**: Unity exports with both Unity Mediation and IronSource LevelPlay include conflicting mediation SDKs with identical package namespaces

**Error Messages**:
```
Duplicate class found in modules:
- com.unity3d.mediation:mediation-sdk:[1.0,2.0[
- com.unity3d.ads-mediation:mediation-sdk:8.11.1
```

**Root Cause**: Unity 2022.3.62f1+ exports can include both legacy Unity Mediation SDK and newer IronSource mediation SDK that use the same namespace but different Maven coordinates.

**File Fixed**: `unityLibrary/build.gradle`

**Solution**:

1. **Identify the conflict** - Look for both mediation dependencies:
```gradle
// Look for these two conflicting dependencies:
implementation 'com.unity3d.mediation:mediation-sdk:[1.0,2.0[' // Legacy Unity Mediation
implementation 'com.unity3d.ads-mediation:mediation-sdk:8.11.1' // IronSource LevelPlay
```

2. **Exclude conflicting legacy Unity mediation SDK**:
```gradle
// Comment out or exclude the legacy Unity mediation SDK
// implementation 'com.unity3d.mediation:mediation-sdk:[1.0,2.0[' // EXCLUDED: Conflicts with IronSource mediation SDK
```

3. **Keep IronSource mediation SDK**:
```gradle 
implementation 'com.unity3d.ads-mediation:mediation-sdk:8.11.1' // IronSource LevelPlay mediation
```

4. **Force resolution to prevent conflicts**:
```gradle
android {
    configurations.all {
        resolutionStrategy {
            // Force newer IronSource mediation SDK to resolve duplicate classes
            force 'com.unity3d.ads-mediation:mediation-sdk:8.11.1'
        }
    }
}
```

**Why This Happens**: Recent Unity versions include improved mediation through IronSource LevelPlay while still maintaining legacy Unity Mediation references, causing namespace conflicts during build.

**Impact**:
- **Critical** - Blocks all builds until resolved
- **Unity Version Specific** - Affects Unity 2022.3.62f1+ with dual mediation systems
- **Resolution** - Must exclude one SDK to prevent namespace conflicts

### 3.5 Install Referrer Library Version Mismatch
**Problem**: Unity exports bundle `installreferrer-1.0.aar` in `unityLibrary/libs/`, but Unity Ads SDK 4.17.0+ requires Install Referrer 2.1+ which has `getInstallBeginTimestampServerSeconds()`

**Error Message**:
```
java.lang.NoSuchMethodError: No virtual method getInstallBeginTimestampServerSeconds()J 
in class Lcom/android/installreferrer/api/ReferrerDetails;
```

**File Fixed**: `unityLibrary/build.gradle`

**Solution** — replace the local AAR with the Maven dependency:
```gradle
// REMOVE this line:
// implementation(name: 'installreferrer-1.0', ext:'aar')

// ADD this line:
implementation 'com.android.installreferrer:installreferrer:2.2'
```

**Why This Happens**: Unity bundles an old Install Referrer AAR (v1.0) that predates the API methods Unity Ads 4.17.0 expects. The app builds fine but crashes at runtime when Unity Ads tries to call the missing method.

## 4. Android Manifest & Permissions

### 4.1 AD_ID Permission for Android 13+
**Problem**: Missing required permission for advertising on API 33+

**File Fixed**: `unityLibrary/src/main/AndroidManifest.xml`

**Solution**:
```xml
<uses-permission android:name="com.android.vending.BILLING" />
<uses-permission android:name="com.google.android.gms.permission.AD_ID" />  <!-- Add this -->
```

**Why Required**: Google Play policy requires AD_ID permission for apps targeting API 33+ that display advertising.

### 4.2 Unity Activity Configuration
**Problem**: Launcher manifest missing Unity activity declaration causing app launch failures

**File Fixed**: `launcher/src/main/AndroidManifest.xml`

**Solution**:
```xml
<application android:name="androidx.multidex.MultiDexApplication">
  <activity android:name="com.unity3d.player.UnityPlayerActivity" 
            android:label="@string/app_name" 
            android:screenOrientation="userPortrait" 
            android:launchMode="singleTask" 
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale|layoutDirection|density" 
            android:resizeableActivity="false" 
            android:hardwareAccelerated="true" 
            android:exported="true">
    <intent-filter>
      <category android:name="android.intent.category.LAUNCHER" />
      <action android:name="android.intent.action.MAIN" />
    </intent-filter>
    <meta-data android:name="unityplayer.ForwardNativeEventsToDalvik" android:value="true" />
  </activity>
</application>
```

**Why This Happens**: Unity sometimes exports launcher manifests without the required Unity activity declaration.

### 4.3 Firebase Manifest Conflicts
**Problem**: Firebase service exported attribute conflicts between modules

**Error Message**:
```
Attribute service#com.google.firebase.messaging.MessageForwardingService@exported value=(false) from [:unityLibrary] is also present at [:firebase-messaging-cpp:] value=(true)
```

**File Fixed**: `unityLibrary/src/main/AndroidManifest.xml`

⚠️ **IMPORTANT: Line likely EXISTS but is INCOMPLETE**

Unity exports this line WITHOUT the `tools:replace` attribute. You must ADD the attribute to the existing line.

**What Unity exports (INCOMPLETE — will fail)**:
```xml
<service android:name="com.google.firebase.messaging.MessageForwardingService" 
         android:permission="android.permission.BIND_JOB_SERVICE" 
         android:exported="false" />
```

**What it MUST be (COMPLETE — add `tools:replace`)**:
```xml
<service android:name="com.google.firebase.messaging.MessageForwardingService" 
         android:permission="android.permission.BIND_JOB_SERVICE" 
         android:exported="false" 
         tools:replace="android:exported" />
```

**How to Fix**:
1. Search for `MessageForwardingService` in `unityLibrary/src/main/AndroidManifest.xml`
2. Check if `tools:replace="android:exported"` attribute exists
3. If missing, ADD it to the existing `<service>` tag
4. Do NOT add a duplicate service line

**Why This Happens**: Newer Firebase SDK has different exported service settings than Unity's bundled version, requiring explicit conflict resolution via `tools:replace`.

### 4.4 Manifest Property removeAll xmlns Conflict
**Problem**: Unity 2022.3.62f3 exports a `<property>` tag with a redundant `xmlns:tools` declaration that the manifest merger rejects

**Error Message**:
```
Element property at AndroidManifest.xml annotated with 'tools:node="removeAll"' cannot have other attributes : xmlns:tools
```

**File Fixed**: `unityLibrary/src/main/AndroidManifest.xml`

**What Unity exports (BROKEN)**:
```xml
<property tools:node="removeAll" xmlns:tools="http://schemas.android.com/tools" />
```

**Solution** — remove the redundant `xmlns:tools` (already declared on `<manifest>`):
```xml
<property tools:node="removeAll" />
```

**Why This Happens**: Unity duplicates the `xmlns:tools` namespace declaration on the `<property>` element. AGP 8.11+ manifest merger treats extra attributes on `tools:node="removeAll"` elements as errors.

### 4.5 Missing provider_paths.xml Resource
**Problem**: Unity exports AndroidManifest with a FileProvider referencing `@xml/provider_paths` but doesn't create the resource file

**Error Message**:
```
AAPT: error: resource xml/provider_paths (aka com.package.name:xml/provider_paths) not found
```

**File Fixed**: Create `unityLibrary/src/main/res/xml/provider_paths.xml`

**Solution**:
```xml
<?xml version="1.0" encoding="utf-8"?>
<paths>
    <external-path name="external_files" path="." />
    <files-path name="internal_files" path="." />
    <cache-path name="cache_files" path="." />
</paths>
```

**Why This Happens**: The FileProvider declaration in the manifest expects a paths resource that Unity doesn't include in the export.

### 4.6 Launcher Activity hardwareAccelerated Conflict
**Problem**: Launcher manifest activity declares `hardwareAccelerated="true"` but unityLibrary declares `hardwareAccelerated="false"`, causing manifest merger failure

**Error Message**:
```
Suggestion: add 'tools:replace="android:hardwareAccelerated"' to <activity> element to override
```

**File Fixed**: `launcher/src/main/AndroidManifest.xml`

**Solution** — add `tools:replace` to the activity in launcher manifest:
```xml
<activity android:name="com.unity3d.player.UnityPlayerActivity"
          android:hardwareAccelerated="true"
          android:exported="true"
          tools:replace="android:hardwareAccelerated">
```

**Why This Happens**: The launcher and unityLibrary manifests declare different values for `hardwareAccelerated` on the same activity, and the manifest merger requires an explicit override.

### 4.7 Launcher flatDir AAR Resolution
**Problem**: Launcher module cannot resolve AAR dependencies from unityLibrary/libs/ when `dependencyResolutionManagement` is removed from settings.gradle

**Error Message**:
```
Could not find :installreferrer-1.0:
Could not find :PaperPlaneToolsAlert:
Could not find :androidgoodieslib-release:
Could not find :firebase-messaging-cpp:
```

**File Fixed**: `launcher/build.gradle`

**Solution** — add a `repositories` block to launcher/build.gradle:
```gradle
repositories {
    flatDir {
        dirs project(':unityLibrary').file('libs')
    }
}
```

**Why This Happens**: The `allprojects` block in unityLibrary/build.gradle sets `flatDir { dirs 'libs' }` which resolves relative to each module's own directory. The launcher module's `libs/` doesn't contain the AARs — they live in `unityLibrary/libs/`. An explicit cross-module flatDir reference is needed.

## 5. Build Optimization & Packaging

### 5.1 Resource Pattern Fix (APK/AAB Builds)
**Problem**: Malformed noCompress patterns cause AAB build failures

**Error**: AAB builds fail with malformed glob pattern syntax

**Files Fixed**:
- `launcher/build.gradle`
- `unityLibrary/build.gradle`

**Unity generates broken syntax**:
```gradle
// BROKEN - Unity export generates this malformed pattern
noCompress '[\'.unity3d\', \'.ress\', \'.resource\', \'.obb\', \'.bundle\', \'.unityexp\'] + unityStreamingAssets.tokenize(\', \')'
```

**Solution**:
```gradle
androidResources {
    ignoreAssetsPattern '!.svn:!.git:!.ds_store:!*.scc:.*:!CVS:!thumbs.db:!picasa.ini:!*~'
    noCompress '.unity3d', '.ress', '.resource', '.obb', '.bundle', '.unityexp'  // Fixed: Simple comma-separated list
}

packagingOptions {
    jniLibs {
        useLegacyPackaging true  // Required for Unity IL2CPP - extracts native libs to disk
        keepDebugSymbols += ['*/armeabi-v7a/*.so', '*/arm64-v8a/*.so']
    }
}
```

**Critical Differences**:
- **APK builds**: Tolerate malformed patterns (with warnings)
- **AAB builds**: Fail completely on malformed patterns - require exact syntax

**useLegacyPackaging**: Must be `true` for Unity IL2CPP apps. Setting to `false` causes `libil2cpp.so` to not be extracted, resulting in a runtime crash (`dlopen failed: library "libil2cpp.so" not found`).

### 5.2 MultiDex Configuration
**Problem**: App crashes immediately on launch with ClassNotFoundException

**Error Message**:
```
Unable to instantiate application androidx.multidex.MultiDexApplication
Caused by: java.lang.ClassNotFoundException: Didn't find class "androidx.multidex.MultiDexApplication"
```

**File Fixed**: `launcher/build.gradle`

**Solution**:

1. **Add MultiDex dependency**:
```gradle
dependencies {
    implementation project(':unityLibrary')
    implementation 'androidx.multidex:multidex:2.0.1'  // Add this
}
```

2. **Enable MultiDex support**:
```gradle
defaultConfig {
    minSdkVersion 28
    targetSdkVersion 35
    multiDexEnabled true  // Add this
    // ... rest of config
}
```

**Why This Happens**: Unity Android exports sometimes reference MultiDexApplication in manifest without including the required dependency.

### 5.3 Minification & ProGuard Rules
**Problem**: R8 minification strips required Unity plugin classes causing runtime crashes

**File Fixed**: `unityLibrary/proguard-unity.txt`

**Solution**:
```proguard
# Preserve Unity plugin classes
-keep class com.amplitude.** { *; }
-keep class com.appsflyer.** { *; }
-keep class com.ironsource.** { *; }
-keep class com.revenuecat.** { *; }
-keep class com.onevcat.** { *; }

# SQLite classes (for Unity's database dependencies)
-keep class org.sqlite.** { *; }
-keep class android.database.sqlite.** { *; }

# Google Play Games (if using authentication)
-keep class com.google.games.** { *; }
-keep class com.google.android.gms.games.** { *; }
```

**Alternative**: Disable minification entirely if ProGuard rules become complex:
```gradle
buildTypes {
    release {
        minifyEnabled false  // Disable if rules get too complex
    }
}
```

## 6. Google Play Compliance

### 6.1 16KB Page Size Alignment Fix
**Problem**: Native libraries not aligned for 16KB page size devices (Google Play requirement November 1, 2025)

**Error Message**:
```
APK is not compatible with 16 KB devices. Some libraries have LOAD segments not aligned at 16 KB boundaries:
lib/arm64-v8a/liba3b9a2.so
lib/arm64-v8a/liblofelt_sdk.so
lib/arm64-v8a/libnms.so  
lib/arm64-v8a/libtobEmbedPagEncrypt.so
```

**Critical Libraries Requiring Fix**:
- `liba3b9a2.so` - Unity/IronSource dependencies (appears in newer exports)
- `liblofelt_sdk.so` - LofeltHaptics.aar (haptic feedback)
- `libnms.so` - Unity/IronSource dependencies  
- `libtobEmbedPagEncrypt.so` - Unity/advertising dependencies

**Implementation**:

1. **Copy Python alignment script** (`fix_elf_alignment.py`) to project root - script available in skill scripts folder

2. **Create Gradle task** (`fix_16kb_alignment.gradle` in project root):
```gradle
// Gradle task to fix 16KB page size alignment for native libraries
// This script calls a local Python file to modify ELF headers for Google Play compliance

task fix16KBAlignment {
    doLast {
        def problematicLibs = [
            "liba3b9a2.so",      // Unity/IronSource (newer exports)
            "liblofelt_sdk.so",  // LofeltHaptics.aar
            "libnms.so",         // Unity/IronSource
            "libtobEmbedPagEncrypt.so"  // Unity/advertising
        ]
        
        def architectures = ["arm64-v8a", "armeabi-v7a"]
        
        architectures.each { arch ->
            problematicLibs.each { libName ->
                def libPath = file("build/intermediates/stripped_native_libs/release/stripReleaseDebugSymbols/out/lib/${arch}/${libName}")
                if (libPath.exists()) {
                    println "Fixing 16KB alignment for ${arch}/${libName}"
                    // Use local Python script for ELF alignment fix
                    exec {
                        commandLine "/usr/bin/python3", 
                                   project.rootProject.file("fix_elf_alignment.py").absolutePath, 
                                   libPath.absolutePath
                    }
                } else {
                    println "Library not found (will be skipped): ${arch}/${libName}"
                }
            }
        }
    }
}

// Run after native libraries are stripped but before APK/AAB packaging
afterEvaluate {
    if (project.tasks.findByName('stripReleaseDebugSymbols')) {
        project.stripReleaseDebugSymbols.finalizedBy fix16KBAlignment
    }
    if (project.tasks.findByName('stripDebugDebugSymbols')) {
        project.stripDebugDebugSymbols.finalizedBy fix16KBAlignment
    }
}
```

3. **Apply to build process** (`launcher/build.gradle`):
```gradle
apply plugin: 'com.android.application'
apply from: '../fix_16kb_alignment.gradle'  // Add this line
```

**How It Works**:
- Python script (`fix_elf_alignment.py`) handles ELF header modification with full error handling and backup creation
- Automatically runs during build after native libraries are processed
- Changes LOAD segment alignment from 4KB (0x1000) to 16KB (0x4000) 
- Supports both 32-bit (armeabi-v7a) and 64-bit (arm64-v8a) architectures

**Verification**: Look for these messages in build output:
```
> Task :launcher:fix16KBAlignment
Fixing 16KB alignment for arm64-v8a/liblofelt_sdk.so
Processing: /path/to/build/intermediates/stripped_native_libs/release/stripReleaseDebugSymbols/out/lib/arm64-v8a/liblofelt_sdk.so
64-bit ELF detected
LOAD segment 0: current alignment = 0x1000
  Fixing alignment: 0x1000 -> 0x4000 (16KB)
Successfully fixed 1 LOAD segments
```

**Google Play Timeline**: This fix becomes mandatory November 1, 2025 for all new apps and updates targeting Android 15+ devices.

### 6.2 Signing Configuration
**Problem**: Incorrect keystore paths or missing passwords preventing release builds

**File Fixed**: `launcher/build.gradle`

**Solution**:
```gradle
signingConfigs {
    release {
        storeFile file('/path/to/your/keystore.keystore')  // Update with correct path
        storePassword 'your_store_password'
        keyAlias 'your_key_alias' 
        keyPassword 'your_key_password'
    }
}

buildTypes {
    release {
        signingConfig signingConfigs.release
        // ... other release settings
    }
}
```

**Security Best Practice** - Use gradle.properties for passwords:

1. **Create gradle.properties** (add to .gitignore):
```properties
KEYSTORE_PASSWORD=your_store_password
KEY_PASSWORD=your_key_password
```

2. **Reference in build.gradle**:
```gradle
signingConfigs {
    release {
        storeFile file('/path/to/your/keystore.keystore')
        storePassword project.hasProperty('KEYSTORE_PASSWORD') ? KEYSTORE_PASSWORD : ''
        keyAlias 'your_key_alias'
        keyPassword project.hasProperty('KEY_PASSWORD') ? KEY_PASSWORD : ''
    }
}
```

**Common Issues**:
- Wrong keystore path (check if file exists)
- Missing both storePassword AND keyPassword
- Keystore alias mismatch

## Build Output Locations

### Generated Files
| Build Type | Output Location | Description |
|-----------|----------------|-------------|
| **APK** | `launcher/build/outputs/apk/release/launcher-release.apk` | Release APK for sideloading |
| **AAB** | `launcher/build/outputs/bundle/release/launcher-release.aab` | Google Play bundle |
| **Debug Symbols** | `launcher/build/outputs/native-debug-symbols/release/` | For crash analysis |
| **ProGuard Mapping** | `launcher/build/outputs/mapping/release/mapping.txt` | For deobfuscation |

### Verification Commands
```bash
# Check APK alignment after build
"/path/to/Android/sdk/build-tools/35.0.0/aapt" dump badging launcher/build/outputs/apk/release/launcher-release.apk | grep -E "(package|targetSdkVersion)"

# Verify AAB contents
"/path/to/Android/sdk/tools/bin/bundletool" validate --bundle=launcher/build/outputs/bundle/release/launcher-release.aab
```

## Troubleshooting

### Common Build Failures

1. **Sync Issues**:
   ```
   File → Invalidate Caches → Invalidate and Restart
   ```

2. **SDK License Errors**:
   ```bash
   /path/to/Android/sdk/cmdline-tools/latest/bin/sdkmanager --licenses
   ```

3. **Gradle Cache Issues**:
   ```bash
   # Stop Gradle daemon
   ./gradlew --stop
   
   # Clear Gradle cache  
   rm -rf ~/.gradle/caches/
   rm -rf .gradle/
   
   # Resync project
   ./gradlew clean
   ```

4. **NDK Path Issues**:
   ```bash
   # Verify NDK installation
   ls "/path/to/Android/sdk/ndk/27.0.12077973"
   
   # Check local.properties
   cat local.properties
   ```

### Build Verification Steps

1. **Clean Build Test**:
   ```bash
   ./gradlew clean
   ./gradlew assembleRelease
   ```

2. **AAB Build Test**:
   ```bash
   ./gradlew clean  
   ./gradlew bundleRelease
   ```

3. **Dependency Conflict Check**:
   ```bash
   ./gradlew dependencies --configuration releaseRuntimeClasspath > dependencies.txt
   # Review dependencies.txt for conflicts
   ```

4. **16KB Alignment Verification**:
   ```bash
   # Look for this in build output:
   # > Task :launcher:fix16KBAlignment
   # Fixing 16KB alignment for arm64-v8a/liblofelt_sdk.so
   ```

### Google Play Console Warnings

#### Warning 1: Unused Code and Resources
- **For APK uploads**: Can be safely ignored
- **For AAB uploads**: Automatically optimized by Google Play

#### Warning 2: Missing Deobfuscation File
- **With minification OFF**: Informational only, can ignore
- **With minification ON**: Upload `mapping.txt` from build outputs

#### Warning 3: Missing Debug Symbols
- **Recommended**: Upload `native-debug-symbols.zip` to Google Play Console
- **Location**: `build/outputs/native-debug-symbols/release/`
- **Benefit**: Readable crash reports instead of memory addresses

## Google Play Submission Checklist

### Pre-Submission Verification
- ✅ **Target API 35+** - Required for new apps (August 2025+)
- ✅ **16KB page size compatibility** - Required November 1, 2025
- ✅ **Updated IronSource Ad Quality SDK** - Version 7.19.2+ (critical)
- ✅ **AD_ID permission included** - Required for advertising apps
- ✅ **AAB format generated successfully** - Preferred by Google Play
- ✅ **Debug symbols prepared** - For crash analysis
- ✅ **Signing configuration working** - Both keystore passwords set

### Upload Process

1. **Google Play Console → App Bundle Explorer**
2. **Upload AAB file** (preferred) or APK  
3. **Upload debug symbols** (recommended)
4. **Add release notes**
5. **Configure rollout percentage**

### Google Play Games Integration
If using Google Play Games authentication:

1. **Upload to Internal Testing first** - Certificate fingerprint auto-registers
2. **Add test accounts** - Resolves authentication errors
3. **Test authentication flow** - Before production release

## Future Unity Exports

### Expected Issues
These fixes will be required for most Unity 2022.3+ Android exports until Unity improves their export process. Unity 6 LTS may have better Android 15+ support when available.

### Unity Export Settings Checklist
- ✅ **Use "Export for App Bundle"** - When planning AAB submission
- ✅ **Target API Level 35** - For Google Play compliance  
- ✅ **Uncheck "Development Build"** - For release builds
- ✅ **IL2CPP Backend** - Required for production apps

### Automation Tips

1. **Save This Guide** - Apply systematically to new exports
2. **Create Custom Gradle Templates** - Enable in Unity's Publishing Settings
3. **Version Control** - Track working build.gradle configurations
4. **Copy 16KB Fix Scripts** - To each new Unity export project

### Unity Version Considerations

| Unity Version | NDK Required | Status | Notes |
|---------------|-------------|--------|-------|
| 2022.3.x LTS  | 27.0.12077973 | ✅ Recommended | Current LTS, most stable for Android 15 |
| Unity 6 LTS   | TBD | 🔄 Future | Next LTS target, better Android 15+ support expected |

### Preventive Measures

1. **Monitor SDK Updates** - Keep advertising SDKs current
2. **Test Both APK and AAB** - Before major releases
3. **Validate on Internal Testing** - Before production uploads
4. **Keep Alignment Scripts Updated** - Add new problematic libraries as discovered

**This comprehensive guide covers all known Unity Android export issues for Google Play Store submission. Keep this documentation updated as new Unity versions and Google Play requirements emerge.**
