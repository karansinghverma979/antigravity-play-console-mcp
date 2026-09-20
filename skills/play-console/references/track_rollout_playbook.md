# 🚀 Android Track Rollout Playbook

## 1. Track Hierarchy & Promotion Path

```text
[Internal Test Track]  ──(Smoke Test)──>  [Closed / Beta Track]  ──(Staged Rollout)──>  [Production Track]
   • Fast distribution                      • Target test groups                           • 10% -> 25% -> 50% -> 100%
   • Up to 100 testers                       • Wider feedback                               • Real end users
```

---

## 2. Release Status Values
- **`draft`**: Release is saved in Play Console but not visible to users. Good for staged validation.
- **`inProgress`**: Active staged rollout. Requires `user_fraction` (e.g. `0.1` for 10%).
- **`completed`**: 100% rollout to all users on the target track.
- **`halted`**: Rollout has been paused due to detected crash spikes or critical defects.

---

## 3. Recommended Phased Rollout Schedule for Production
1. **Day 1**: Deploy with `user_fraction: 0.05` (5%) or `0.10` (10%).
2. **Day 2**: Monitor Crashlytics and Google Play Android Vitals for ANRs or crash-free user rate drops.
3. **Day 3**: If stable, update release to `user_fraction: 0.25` (25%).
4. **Day 5**: Increase to `user_fraction: 0.50` (50%).
5. **Day 7**: Complete release with `status: "completed"`.
