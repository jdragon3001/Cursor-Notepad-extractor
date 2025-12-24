# Frontend Testing Guide - Temporal Filtering

## Quick Start

Your frontend and backend are already running from `deploy.ps1`:
- **Backend:** http://127.0.0.1:8000
- **Frontend:** http://localhost:5173

Just open your browser to http://localhost:5173 to test!

---

## Test Checklist

### 1. Time Range Selector Tests

#### Test Preset Buttons:
- [ ] Click "All Time" - Stats show all data
- [ ] Click "Last 7 Days" - Stats reduce (should show ~4,400 messages)
- [ ] Click "Last 30 Days" - Stats reduce (should show ~20,524 messages)
- [ ] Click "Last 90 Days" - Stats increase from 30 days

#### Test More Options:
- [ ] Click "More" button - Dropdown opens
- [ ] Click "This Month" - Shows December 2025 stats
- [ ] Click "Last Month" - Shows November 2025 stats
- [ ] Click "This Year" - Shows 2025 stats
- [ ] Click outside dropdown - Dropdown closes

#### Test Custom Date Range:
- [ ] Click "More" → Scroll to "Custom Range"
- [ ] Select start date (e.g., 2025-12-01)
- [ ] Select end date (e.g., 2025-12-15)
- [ ] Click "Apply Custom Range"
- [ ] Verify stats update for that range

---

### 2. Stat Card Tests

#### Test Clickable Stats:
- [ ] Hover over any stat card - Background changes
- [ ] Click "Total Messages" card - Modal opens
- [ ] Click "Total Sessions" card - Modal opens
- [ ] Click any message stat - Modal opens
- [ ] Click any session stat - Modal opens

---

### 3. Drill-Down Modal Tests

#### Test Modal Opening:
- [ ] Modal appears centered on screen
- [ ] Modal has gradient blue header
- [ ] Current value displays prominently
- [ ] Trend indicator shows (up/down/stable)
- [ ] Time series chart renders

#### Test Time Range Controls:
- [ ] Change time range dropdown to "Last 7 Days"
  - Chart updates with 7 days of data
  - Data points refresh
- [ ] Change to "Last 90 Days"
  - Chart shows more data points
  - X-axis labels adjust

#### Test Granularity Controls:
- [ ] Set to "Daily" - Shows day-by-day data
- [ ] Set to "Weekly" - Groups data by week
- [ ] Set to "Monthly" - Groups data by month
- [ ] Verify chart updates each time

#### Test Chart Interactions:
- [ ] Hover over chart points - Tooltip shows value
- [ ] Hover over line - Highlights
- [ ] Chart is responsive to window size

#### Test Modal Closing:
- [ ] Click X button - Modal closes
- [ ] Click "Close" button - Modal closes
- [ ] Click outside modal - Modal closes
- [ ] Keyboard ESC - Modal closes (if implemented)

---

### 4. Integration Tests

#### Test Combined Functionality:
- [ ] Set time range to "Last 30 Days"
- [ ] Verify summary cards show unfiltered totals
- [ ] Verify stat cards show filtered counts
- [ ] Click a stat card
- [ ] Modal opens with Last 30 Days data
- [ ] Change modal to "Last 7 Days"
- [ ] Chart updates correctly
- [ ] Close modal
- [ ] Main page still shows Last 30 Days filter

#### Test Search + Time Filter:
- [ ] Set time range to "Last 30 Days"
- [ ] Type "message" in search box
- [ ] Verify only message stats show
- [ ] All are filtered by last 30 days
- [ ] Change to "All Time"
- [ ] Stats update but search filter remains

---

### 5. Visual/UX Tests

#### Layout & Design:
- [ ] Time range selector looks good
- [ ] Preset buttons have proper spacing
- [ ] Modal is well-designed
- [ ] Charts are visually appealing
- [ ] Colors match the theme
- [ ] Icons display correctly

#### Responsiveness:
- [ ] Resize browser to mobile width (375px)
  - Time range buttons stack properly
  - Modal fits screen
  - Chart remains readable
- [ ] Test at tablet width (768px)
- [ ] Test at desktop width (1920px)

#### Loading States:
- [ ] When changing time range, stats update smoothly
- [ ] Modal shows loading spinner while fetching data
- [ ] No flickering or layout shifts

---

### 6. Error Handling Tests

#### Test Edge Cases:
- [ ] Select future dates in custom range
  - Should work (no data)
  - Stat values should be 0 or minimal
- [ ] Select start date after end date
  - Should still work (backend handles this)
- [ ] Click stat with no data
  - Modal opens
  - Chart shows "No data available"

---

### 7. Performance Tests

#### Speed Checks:
- [ ] Clicking preset buttons feels instant
- [ ] Modal opens without delay
- [ ] Chart renders quickly (<1 second)
- [ ] Changing granularity is fast
- [ ] No lag when interacting with UI

---

## Expected Behavior

### Time Range Filtering:
- **All Time:** ~71,204 messages, 1,032 sessions
- **Last 30 Days:** ~20,524 messages, 328 sessions
- **Last 7 Days:** ~4,400 messages, 62 sessions
- **Last 90 Days:** More than Last 30 Days

### Modal Behavior:
- Opens smoothly with fade-in animation
- Chart always shows data for selected time range
- Trend indicator calculates from first half vs second half
- Close button always visible and functional

---

## Common Issues & Solutions

### Issue: Stats not updating when changing time range
**Solution:** Check browser console for API errors

### Issue: Modal not opening
**Solution:** Check that backend is running on port 8000

### Issue: Chart not rendering
**Solution:** Recharts library should be installed (npm install recharts)

### Issue: Custom date range not working
**Solution:** Ensure dates are in YYYY-MM-DD format

---

## Browser Console Tests

Open DevTools (F12) and check:

### Network Tab:
- [ ] `/api/stats/all?preset=last_30_days` - Returns 200
- [ ] `/api/stats/time-series/total_messages` - Returns 200
- [ ] Response includes `stats` and `time_range` fields

### Console Tab:
- [ ] No red error messages
- [ ] API calls logged
- [ ] State updates logged (if debugging enabled)

---

## Quick Visual Check

When you first load http://localhost:5173, you should see:

1. **Header:** "Cursor Stats Dashboard" with Refresh button
2. **Time Range Selector:** Row of preset buttons + "More" dropdown
3. **Summary Cards:** 4 cards with totals (Messages, Sessions, Diffs, Workspaces)
4. **Search & Filter Bar:** Search box and type filter dropdown
5. **Category Tabs:** All Stats, MESSAGES, SESSIONS, CODE, DAILY, TOOLS, CONTEXT
6. **Stat Cards:** Grid of stats with hover effects

Click any stat card → Modal should open with chart!

---

## Success Criteria

✅ All preset time ranges work
✅ Custom date range works
✅ Stats update when time range changes
✅ Modal opens on stat click
✅ Chart renders with correct data
✅ Granularity controls work
✅ Modal closes properly
✅ No console errors
✅ UI looks polished
✅ Performance is good

---

If all tests pass, temporal filtering is working perfectly! 🎉

Jack, have fun exploring your Cursor usage patterns over time!

