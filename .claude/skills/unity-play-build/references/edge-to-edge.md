# Android 15 Edge-to-Edge Enforcement Fix

## Overview

Starting with Android 15 (API 35), Google enforces edge-to-edge display by default for all apps targeting API 35 or higher. This can cause UI elements to be hidden behind system bars (status bar, navigation bar) if the app doesn't properly handle window insets.

## The Problem

- **Automatic Enforcement**: Apps targeting API 35 automatically display edge-to-edge on Android 15+ devices
- **Transparent System Bars**: Status bar and navigation bar become transparent by default
- **Hidden UI Elements**: Content can be obscured behind system bars and display cutouts
- **Unity Compatibility**: Unity 2022.3.62f3 may not fully support Android 15's edge-to-edge enforcement

## Impact on Unity Apps

Unity apps have special considerations:
- Unity renders its own fullscreen content with custom safe area handling
- Unity's `render-outside-safearea` and `notch_support` settings may not fully handle API 35 enforcement
- Game UI rendered by Unity may be hidden behind system bars on Android 15+ devices

## Solutions

### Solution 1: Temporary Opt-Out (Currently Implemented) ✅

**Status**: Implemented in all Play builds targeting API 35

**Implementation**:
Create `unityLibrary/src/main/res/values-v35/styles.xml` with:

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
  <style name="BaseUnityTheme" parent="android:Theme.Material.Light.NoActionBar.Fullscreen">
    <item name="android:windowOptOutEdgeToEdgeEnforcement">true</item>
    <!-- Other theme attributes -->
  </style>
</resources>
```

**Pros**:
- ✅ Simple to implement
- ✅ Works immediately with current Unity version (2022.3.62f3)
- ✅ No changes to Unity project required
- ✅ Prevents UI being hidden behind system bars

**Cons**:
- ⚠️ **Temporary solution** - will be removed when targeting API 36 (future Android)
- ⚠️ Only delays the problem, doesn't solve it long-term
- ⚠️ Not a proper edge-to-edge implementation

**Timeline**:
- Works for API 35 (current requirement)
- Will need replacement when API 36 is required (likely 2026-2027)

### Solution 2: Proper Edge-to-Edge Implementation (Future)

**Status**: Not yet implemented - requires Unity plugin development

**Requirements**:
1. Create custom Unity native plugin for Android
2. Implement `enableEdgeToEdge()` in MainActivity
3. Handle window insets programmatically
4. Communicate inset values to Unity game code
5. Adjust Unity UI to respect safe areas on Android 15+

**Implementation Steps** (for future):

1. **Create Native Plugin** (`UnityEdgeToEdgePlugin.java`):
```java
public class UnityEdgeToEdgePlugin {
    public static void enableEdgeToEdge(Activity activity) {
        WindowCompat.setDecorFitsSystemWindows(activity.getWindow(), false);
        EdgeToEdge.enable(activity);
    }
}
```

2. **Modify UnityPlayerActivity** to call plugin on startup

3. **Handle Window Insets**:
```java
ViewCompat.setOnApplyWindowInsetsListener(view, (v, insets) -> {
    Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
    // Send inset values to Unity via SendMessage
    UnityPlayer.UnitySendMessage("GameManager", "OnSystemInsetsChanged",
        systemBars.top + "," + systemBars.bottom);
    return insets;
});
```

4. **Update Unity Safe Area Handling** to use Android 15 inset values

**Pros**:
- ✅ Proper long-term solution
- ✅ Works with future Android versions
- ✅ Full control over edge-to-edge behavior

**Cons**:
- ⚠️ Complex implementation requiring native Android development
- ⚠️ Requires Unity project modifications
- ⚠️ Testing required across multiple Android versions
- ⚠️ May conflict with Unity's built-in safe area handling

## Recommendations

### For Current Builds (2024-2025)
1. ✅ **Use opt-out solution** for all Play builds targeting API 35
2. ✅ Add `values-v35/styles.xml` to all Unity Android exports
3. ✅ Test on Android 15+ devices to verify UI is not obscured
4. ✅ Monitor for Google Play Console warnings about edge-to-edge

### For Future Builds (2026+)
1. ⚠️ **Plan for API 36** when opt-out is removed
2. ⚠️ Wait for Unity to add built-in support for edge-to-edge (check Unity roadmap)
3. ⚠️ If Unity doesn't support it, implement native plugin solution
4. ⚠️ Test early on Android beta releases

### Unity Version Tracking
Monitor Unity releases for edge-to-edge support:
- Unity 2022.3.x: No native support - use opt-out
- Unity 6 LTS: Check release notes for API 35 edge-to-edge support
- Future versions: May include built-in handling

## Testing Checklist

When testing edge-to-edge behavior:
- [ ] Test on Android 15 device (API 35)
- [ ] Verify status bar doesn't cover game UI
- [ ] Verify navigation bar doesn't cover game UI
- [ ] Test on devices with display cutouts (notches)
- [ ] Test in portrait and landscape orientations
- [ ] Verify fullscreen gameplay is not affected
- [ ] Check Unity's safe area is respected

## Additional Resources

**Google Documentation**:
- [Edge-to-Edge Behavior Changes](https://developer.android.com/about/versions/15/behavior-changes-15#edge-to-edge)
- [Display Content Edge-to-Edge](https://developer.android.com/develop/ui/views/layout/edge-to-edge)

**Unity Forums**:
- Search for "Unity Android 15 edge-to-edge" for community solutions
- Check Unity Issue Tracker for official support status

## Build Fix Application

**For new Play builds**, the skill automatically:
1. Creates `values-v35/styles.xml` directory
2. Adds edge-to-edge opt-out to theme
3. Inherits splash screen configuration from `values-v31/styles.xml`
4. Builds AAB with edge-to-edge protection

**Manual application**:
```bash
# Create directory
mkdir -p unityLibrary/src/main/res/values-v35/

# Copy opt-out styles.xml (from this documentation or existing build)
# Build as normal
./gradlew bundleRelease
```

## Conclusion

The temporary opt-out solution provides immediate compatibility with Android 15 (API 35) while giving time to develop a proper long-term solution. This approach:
- ✅ Allows Google Play Store submission today
- ✅ Prevents UI issues on Android 15+ devices
- ✅ Buys time until API 36 requirement (likely 2026-2027)
- ✅ Follows industry best practices for Unity Android apps

**Next action required**: Monitor Unity release notes for native edge-to-edge support before API 36 is required.
