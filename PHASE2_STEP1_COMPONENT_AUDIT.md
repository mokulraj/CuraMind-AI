# PHASE 2 - STEP 1: COMPONENT INVENTORY AUDIT

**Status:** COMPLETE - NO MODIFICATIONS MADE  
**Date:** August 15, 2026  
**Scope:** Full audit of existing components across CSS, templates, and JavaScript

---

## COMPONENT INVENTORY

### BUTTONS

**Existing Implementations:**

1. **`.primary-button`** (DUPLICATED)
   - Defined in: `static/css/imaging.css`, `static/css/medical-records.css`, `static/css/settings.css`, `static/css/password.css`
   - Styles: `padding: 11px 18px`, `border-radius: var(--cm-radius-md)`, `background: var(--cm-primary)`, white text
   - States: `:hover { opacity: 0.92; }`
   - Used in: 20+ templates

2. **`.secondary-button`** (DUPLICATED)
   - Defined in: `static/css/imaging.css`, `static/css/settings.css`, `static/css/password.css`
   - Styles: Border with `--cm-border`, surface background, text color `--cm-text`
   - States: `:hover { border-color: var(--cm-primary); color: var(--cm-primary); }`
   - Used in: 15+ templates

3. **`.danger-button`** (SINGLE)
   - Defined in: `static/css/settings.css` only
   - Styles: Hard-coded colors (#e0bcbc border, #fff5f5 background, #b42318 text)
   - States: `:hover { background: #feecec; }`
   - Used in: settings.html

4. **`.auth-submit`** (INCONSISTENT)
   - Defined in: `static/css/auth.css`
   - Styles: `padding: 13px`, `background: var(--cm-primary)`, white text, full-width
   - States: `:hover { opacity: 0.92; }`, `:active { transform: translateY(1px); }`
   - Inconsistent height and padding from `.primary-button`

5. **`.mobile-menu-button`** (INLINE)
   - Defined in: `static/css/layout.css`
   - No hover/active states defined
   - Used in: base.html, navbar.html

6. **`.notification-button`** (INLINE)
   - Defined in: `static/css/layout.css`
   - No specific styling documented
   - Used in: base.html, navbar.html

7. **`.button.button-primary`** (NON-STANDARD)
   - Found in: `templates/dashboard/home.html` line 48
   - Issue: Uses non-standard class names instead of `.primary-button`
   - This appears to be a legacy pattern

8. **Inline button styles in cards**
   - Found in: `imaging.css` line 453, `medical-records.css` line 366
   - Styles: `.imaging-module-card button { border: 0; background: transparent; color: var(--cm-primary); }`
   - Not reusable across components

**Problems Identified:**
- ❌ Button styles defined in 4 different CSS files (duplication)
- ❌ Inconsistent padding/height (11-13px variations)
- ❌ No consistent variants (tertiary, ghost, icon buttons, etc.)
- ❌ No disabled state styling (only opacity applied globally)
- ❌ No loading state
- ❌ No focus states beyond global :focus-visible
- ❌ Hard-coded danger colors instead of using --cm-danger token
- ❌ Mixed naming convention (.primary-button vs .button.button-primary)
- ❌ Inline button styles not reusable
- ❌ No explicit size variants

---

### CARDS

**Existing Implementations:**

1. **`.dashboard-card`** (GENERAL)
   - Defined in: `static/css/components.css`
   - Styles: `padding: 22px`, `border: 1px solid var(--cm-border)`, `border-radius: var(--cm-radius-lg)`, `background: var(--cm-surface)`, `box-shadow: var(--cm-shadow-sm)`
   - Used in: Settings, password change, notifications

2. **`.stat-card`** (METRICS)
   - Defined in: `static/css/dashboard.css`
   - Styles: `padding: 20px`, same border/radius/shadow as dashboard-card
   - Includes header, label, value, change indicator
   - Variants: `.stat-change.positive`, `.stat-change.warning`
   - Used in: dashboard, appointments, imaging, medical_records, patients, reports, ai_insights

3. **`.appointment-stat-card`** (STATISTICS)
   - Defined in: `static/css/appointments.css`
   - Styles: Identical to `.stat-card` (DUPLICATE)
   - Used in: appointments.html

4. **`.imaging-stat-card`** (STATISTICS)
   - Defined in: `static/css/imaging.css`
   - Styles: Identical to `.stat-card` (DUPLICATE)
   - Used in: imaging.html

5. **`.imaging-module-card`** (MODULE)
   - Defined in: `static/css/imaging.css`
   - Unique structure with custom button styling
   - Has: h3, p, button
   - Used in: imaging.html

6. **`.imaging-upload-card`** (UPLOAD)
   - Defined in: `static/css/imaging.css`
   - Styles: Dashed border, flexbox column, 210px min-height
   - Used in: imaging.html

7. **`.record-stat-card`** (STATISTICS)
   - Defined in: `static/css/medical-records.css`
   - Styles: Identical to `.stat-card` (DUPLICATE)
   - Used in: medical_records.html

8. **`.record-category-card`** (CATEGORY)
   - Defined in: `static/css/medical-records.css`
   - Similar structure to imaging-module-card with button
   - Used in: medical_records.html

9. **`.patient-stat-card`** (STATISTICS)
   - Defined in: `static/css/patients.css`
   - Styles: Identical to `.stat-card` (DUPLICATE)
   - Used in: patients.html

10. **`.report-stat-card`** (STATISTICS)
    - Defined in: `static/css/reports.css`
    - Styles: Identical to `.stat-card` (DUPLICATE)
    - Used in: reports.html

11. **`.ai-stat-card`** (AI STATISTICS)
    - Defined in: `static/css/ai-insights.css`
    - Styles: Identical to `.stat-card` (DUPLICATE)
    - Used in: ai_insights.html

12. **`.auth-card`** (AUTHENTICATION)
    - Defined in: `static/css/auth.css`
    - Styles: `padding: 34px`, `border: 1px solid var(--cm-border)`, `border-radius: var(--cm-radius-lg)`, `background: var(--cm-surface)`, `box-shadow: var(--cm-shadow-md)`
    - Used in: auth/login.html, auth/password_change.html

13. **`.password-card`** (PASSWORD SPECIFIC)
    - Defined in: `static/css/password.css`
    - Styles: Extends `.dashboard-card` with max-width: 720px
    - Used in: auth/password_change.html

**Problems Identified:**
- ❌ Stat cards duplicated 5+ times across different modules
- ❌ No semantic card types (header, footer, actions)
- ❌ No interactive card variant
- ❌ No hover/active states on interactive cards
- ❌ No consistent spacing for card content
- ❌ Module-specific styling not reusable
- ❌ Upload card not generalized
- ❌ No disabled card state
- ❌ No loading/skeleton variant

---

### FORMS & INPUTS

**Existing Implementations:**

1. **`.form-group`** (FIELD CONTAINER)
   - Defined in: Multiple CSS files (settings.css, auth.css, password.css, etc.)
   - Styles: `display: flex; flex-direction: column; gap: 7px`
   - Consistent across files
   - Used in: All forms throughout app

2. **Input Elements** (BASE STYLES)
   - Defined in: `static/css/base.css`
   - Global styles for: `input[type="text"]`, `input[type="email"]`, `input[type="password"]`, `input[type="number"]`, `input[type="date"]`, `input[type="time"]`, `input[type="search"]`, `input[type="url"]`, `input[type="tel"]`, `textarea`, `select`
   - Styles: `padding: 10px 12px`, `border: 1px solid var(--cm-border)`, `border-radius: var(--cm-radius-md)`, `background: var(--cm-surface)`, `color: var(--cm-text)`
   - States: `:focus` with blue border and shadow, `:disabled` with surface-soft background
   - Placeholder: `color: var(--cm-text-muted)`

3. **Auth Form Inputs** (MODULE-SPECIFIC)
   - Defined in: `static/css/auth.css`
   - Overrides base styles with: `padding: 12px 13px`, `background: var(--cm-surface-soft)`
   - Focus state has custom shadow: `0 0 0 3px rgba(37, 99, 235, 0.1)`
   - Used in: auth/login.html

4. **Password Form Inputs** (MODULE-SPECIFIC)
   - Defined in: `static/css/password.css`
   - Styles: `padding: 11px 12px`, `background: var(--cm-bg)`
   - Slightly different from base and auth forms (INCONSISTENT)
   - Used in: auth/password_change.html

5. **Patient Search Input** (MODULE-SPECIFIC)
   - Defined in: `static/css/patients.css`
   - Styles: `width: 250px`, `padding: 10px 13px`, `background: var(--cm-bg)`
   - Fixed width, not responsive (ISSUE)
   - Used in: patients.html

6. **Imaging Search Input** (MODULE-SPECIFIC)
   - Defined in: `static/css/imaging.css`
   - Similar to patient search
   - Fixed width 250px (ISSUE)
   - Used in: imaging.html

7. **Medical Records Search Input** (MODULE-SPECIFIC)
   - Defined in: `static/css/medical-records.css`
   - Similar to patient search
   - Fixed width 250px (ISSUE)
   - Used in: medical_records.html

8. **Form Error Display**
   - Defined in: `static/css/password.css`, auth.css
   - `.form-error`: `padding: 11px 13px`, hard-coded background/border/text
   - `.field-error`: `color: #b42318` (hard-coded, not using --cm-danger)
   - Used in: auth forms, password change, settings

9. **Help Text**
   - Defined in: `static/css/password.css`
   - `.password-help`: `-8px margin-top`, secondary text color
   - Used in: password change form

10. **Settings Form Grid** (LAYOUT)
    - Defined in: `static/css/settings.css`
    - `.settings-form-grid`: `grid-template-columns: repeat(2, minmax(0, 1fr))`, `gap: 18px`
    - Responsive: `@media (max-width: 700px) { grid-template-columns: 1fr; }`
    - Used in: settings.html, add_patient.html

**Problems Identified:**
- ❌ Input padding inconsistent across modules (10px, 11px, 12px, 13px variations)
- ❌ Input background color variations (--cm-surface vs --cm-surface-soft vs --cm-bg)
- ❌ Search inputs have fixed width (not responsive)
- ❌ Error messages use hard-coded colors instead of --cm-danger
- ❌ No separate styling for required fields
- ❌ No validation success state
- ❌ No input size variants (small, medium, large)
- ❌ Help text not consistently positioned
- ❌ No focus ring consistency across input types
- ❌ Textarea has no specific styling for resize handle
- ❌ No inline validation message styling

---

### STATUS BADGES/BADGES

**Existing Implementations:**

1. **`.appointment-status`** (APPOINTMENT SPECIFIC)
   - Defined in: `static/css/appointments.css`
   - Base: `padding: 5px 9px`, `border-radius: 999px`, `font-size: 11px`, `font-weight: 600`
   - Variants:
     - `.appointment-status.confirmed`: `background: var(--cm-primary-soft)`, `color: var(--cm-primary)`
     - `.appointment-status.pending`: `background: #fff4d6`, `color: #9a6700` (hard-coded)
   - Used in: appointments.html

2. **`.patient-status`** (PATIENT SPECIFIC)
   - Defined in: `static/css/patients.css`
   - Base: `padding: 5px 9px`, `border-radius: 999px`, `font-size: 11px`, `font-weight: 600`
   - Variants:
     - `.patient-status.active`: `background: var(--cm-primary-soft)`, `color: var(--cm-primary)`
     - `.patient-status.inactive`: `background: #f1f1f1`, `color: #666` (hard-coded)
   - Used in: patients.html

3. **`.ai-badge`** (AI SPECIFIC)
   - Defined in: `static/css/imaging.css`
   - Variants:
     - `.ai-badge.completed`: `background: var(--cm-primary-soft)`, `color: var(--cm-primary)`
     - `.ai-badge.processing`: `background: #fff4d6`, `color: #9a6700` (hard-coded)
   - Used in: imaging.html

4. **`.study-status`** (IMAGING SPECIFIC)
   - Defined in: `static/css/imaging.css`
   - Variants: `.study-status.reviewed`, `.study-status.pending` (styles not shown in audit)
   - Used in: imaging.html

5. **`.record-status`** (RECORDS SPECIFIC)
   - Defined in: `static/css/medical-records.css`
   - Base same as appointment-status
   - Variants: `.record-status.reviewed`, `.record-status.pending` (hard-coded colors likely)
   - Used in: medical_records.html

6. **`.report-status`** (REPORTS SPECIFIC)
   - Defined in: `static/css/reports.css`
   - Variants: `.report-status.completed`, `.report-status.review`, `.report-status.draft`
   - Used in: reports.html

7. **`.notification-badge`** (NOTIFICATION COUNT)
   - Defined in: `static/css/layout.css`
   - Used in: navbar.html to show notification count
   - Styling not detailed in audit

**Problems Identified:**
- ❌ Status badges duplicated across modules with identical base styles
- ❌ No unified semantic status system
- ❌ Hard-coded colors for pending/processing instead of --cm-warning
- ❌ No size variants (small, medium, large)
- ❌ No icon support in badges
- ❌ No animation for status changes
- ❌ Inconsistent naming (badge vs status)
- ❌ No dismissed/archive state
- ❌ No loading/processing animation

---

### TABLES

**Existing Implementations:**

1. **`.appointment-table-wrapper`** + `.appointment-table`
   - Defined in: `static/css/appointments.css`
   - Wrapper: `overflow-x: auto` (scrollable)
   - Table: `width: 100%`, `border-collapse: collapse`
   - Cells: `padding: 14px 10px`, `border-bottom: 1px solid var(--cm-border)`, `text-align: left`
   - Headers: Secondary text color, uppercase, small font
   - Used in: appointments.html

2. **`.patient-table-wrapper`** + `.patient-table`
   - Defined in: `static/css/patients.css`
   - Identical structure to appointment table (DUPLICATE)
   - Used in: patients.html

3. **`.imaging-table-wrapper`** + `.imaging-table`
   - Defined in: `static/css/imaging.css`
   - Identical structure (DUPLICATE)
   - Includes study-icon styling
   - Used in: imaging.html

4. **`.activity-table-wrapper`** + `.activity-table`
   - Defined in: `static/css/dashboard.css`
   - Identical structure (DUPLICATE)
   - Used in: dashboard/home.html, dashboard/index.html

5. **`.report-table-wrapper`** + `.report-table`
   - Defined in: `static/css/reports.css`
   - Identical structure (DUPLICATE)
   - Used in: reports.html

6. **Medical Records List** (NOT A TABLE)
   - Defined in: `static/css/medical-records.css`
   - Uses `.records-list` container
   - Uses `.record-item` rows
   - Styled as list, not table

**Problems Identified:**
- ❌ Table styles duplicated 5+ times
- ❌ No table header sticky positioning
- ❌ No hover row state
- ❌ No row selection/checkbox support
- ❌ No sortable column headers
- ❌ No pagination styling defined
- ❌ Mobile behavior not implemented (tables overflow on mobile)
- ❌ No row action buttons styling
- ❌ No empty table state
- ❌ No loading skeleton for tables

---

### NOTIFICATIONS & ALERTS

**Existing Implementations:**

1. **`.auth-error`** (AUTHENTICATION ERROR)
   - Defined in: `static/css/auth.css`
   - Styles: `padding: 11px 13px`, `border: 1px solid #e5bcbc`, `border-radius: var(--cm-radius-md)`, `background: #fff5f5`, `color: #b42318`
   - Hard-coded red colors (not using --cm-danger token)
   - Used in: auth/login.html, auth/password_change.html

2. **`.form-error`** (FORM ERROR)
   - Defined in: `static/css/password.css`, auth.css
   - Styles: `padding: 11px 13px`, hard-coded background/border/text
   - Same hard-coded red colors
   - Used in: password change, settings

3. **`.field-error`** (INLINE FIELD ERROR)
   - Defined in: `static/css/password.css`, auth.css
   - Styles: `color: #b42318` (hard-coded red)
   - No background or padding
   - Used in: auth forms, settings forms

4. **`.auth-messages`** (MESSAGE CONTAINER)
   - Defined in: `templates/base/auth_base.html`
   - No specific CSS styling found
   - Used in: auth pages

5. **`.site-messages`** (APP MESSAGE CONTAINER)
   - Defined in: `templates/base/base.html`
   - No specific CSS styling found
   - Used in: app pages

6. **Notification Badge** (COUNT INDICATOR)
   - Defined in: navbar styling
   - Shows count of unread notifications
   - Used in: base.html

7. **`.notification-list`** (NOTIFICATION LIST)
   - Defined in: layout styling
   - List container for notifications
   - Used in: notifications/index.html

8. **Empty State** (NO NOTIFICATIONS)
   - Found in: `templates/notifications/index.html`
   - `.empty-state` and `.empty-state-icon` classes defined
   - Minimal styling

**Problems Identified:**
- ❌ Error messages use hard-coded colors instead of --cm-danger
- ❌ No success/success alert component
- ❌ No warning alert component
- ❌ No info alert component
- ❌ No dismissible alert (close button)
- ❌ No alert icon support
- ❌ Message/alert components not reusable
- ❌ No multiple alerts support
- ❌ No toast/temporary notification styling
- ❌ Empty state barely styled

---

### NAVIGATION & LISTS

**Existing Implementations:**

1. **Sidebar Navigation**
   - Defined in: `static/css/layout.css`
   - `.sidebar-link` for navigation items
   - JavaScript selector: `.sidebar-link` with `.active` class
   - No hover state styling documented

2. **Mobile Menu Button**
   - Defined in: `static/css/layout.css`
   - `.mobile-menu-button` class
   - JavaScript toggle for sidebar `.open` class
   - Used in: base.html, navbar.html

3. **User Menu**
   - Found in: `.user-menu` class in templates
   - No specific CSS styling found
   - Used in: base.html

4. **Appointment List**
   - Found in: `.appointment-list` in dashboard
   - Uses `.appointment-item` rows
   - Each item has: time, details, status
   - Used in: dashboard/home.html

5. **Preference List**
   - Found in: `.preference-list` in settings
   - Uses `.preference-item` rows
   - Each item has: label, description, toggle
   - Used in: settings.html

6. **Notification List**
   - Found in: `.notification-list` in notifications
   - Used in: notifications/index.html

7. **Records List**
   - Found in: `.records-list` in medical records
   - Not a table, styled as list
   - Used in: medical_records.html

8. **AI Analysis List**
   - Found in: `.ai-analysis-list` in ai_insights
   - Used in: ai_insights.html

**Problems Identified:**
- ❌ No dropdown menu styling defined
- ❌ No breadcrumb component
- ❌ No tabs/tab navigation
- ❌ No pagination component
- ❌ No accordion component
- ❌ List items not standardized
- ❌ No active/hover states for list items

---

### MODALS & OVERLAYS

**Existing Implementations:**

None found in the codebase during audit.

**Problems Identified:**
- ❌ No modal component
- ❌ No modal backdrop
- ❌ No modal close button
- ❌ No modal focus management
- ❌ No Escape key handler
- ❌ No body scroll lock

---

### AI COMPONENTS

**Existing Implementations:**

1. **`.ai-insight`** (DASHBOARD AI INSIGHT)
   - Defined in: `static/css/dashboard.css`
   - Styles: `display: flex`, `gap: 12px`, `padding: 14px 0`, `border-bottom: 1px solid var(--cm-border)`
   - Contains: icon, strong text, paragraph
   - Used in: dashboard

2. **`.ai-insight-icon`** (INSIGHT ICON)
   - Styles: `width: 34px`, `height: 34px`, flexbox center, `border-radius: 8px`, `background: var(--cm-primary-soft)`
   - Used with dashboard AI insights

3. **`.ai-badge`** (AI STATUS BADGE)
   - Already documented in badges section
   - States: `.ai-badge.completed`, `.ai-badge.processing`
   - Used in: imaging.html

4. **AI Stat Cards**
   - `.ai-stat-card`: Identical to regular stat cards
   - Used in: ai_insights.html

**Problems Identified:**
- ❌ No AI-specific visual language
- ❌ No AI confidence indicator styling
- ❌ No AI processing animation
- ❌ Limited AI component types
- ❌ No AI recommendation card
- ❌ No AI explanation block
- ❌ No AI-generated document indicator

---

### LOADING & EMPTY STATES

**Existing Implementations:**

1. **Empty State** (BASIC)
   - Found in: `templates/notifications/index.html`
   - Classes: `.empty-state`, `.empty-state-icon`
   - Minimal styling
   - HTML structure: icon div, title, explanation text, optional CTA

**Problems Identified:**
- ❌ No loading skeleton component
- ❌ No button loading state animation
- ❌ No table loading skeleton
- ❌ No card loading skeleton
- ❌ Empty states not consistently styled
- ❌ No empty state illustrations
- ❌ Error state not formalized
- ❌ Not found (404) page styling minimal

---

### ACCESSIBILITY ISSUES

**Current Implementation:**

1. **Base ARIA Support**
   - `.skip-link` defined for keyboard navigation
   - JavaScript adds `aria-expanded` to menu toggles
   - No role attributes documented

**Problems Identified:**
- ❌ No semantic HTML5 landmarks consistently used
- ❌ Limited ARIA labels
- ❌ No ARIA live regions for notifications
- ❌ Color-only status indicators (not accessible)
- ❌ No focus indicators on all interactive elements
- ❌ Icon-only buttons lack labels
- ❌ Tables missing header associations
- ❌ Forms missing required field indicators

---

### MOBILE & RESPONSIVE ISSUES

**Current Implementation:**

Breakpoints: 1100px, 850px, 800px, 700px, 600px, 500px (INCONSISTENT)

**Problems Identified:**
- ❌ No consistent mobile breakpoint strategy
- ❌ Search inputs have fixed widths (not responsive)
- ❌ Tables overflow horizontally on mobile (no card transformation)
- ❌ Buttons may not meet 44x44px touch target on mobile
- ❌ Forms not optimized for mobile (2-column grids collapse to 1)
- ❌ Menu button positioning inconsistent
- ❌ Modals would overflow viewport

---

### DUPLICATE CSS DEFINITIONS

The following CSS classes are defined in multiple files (causing maintenance issues):

1. **`.primary-button`** - Defined in: imaging.css, medical-records.css, settings.css, password.css (4 files)
2. **`.secondary-button`** - Defined in: imaging.css, settings.css, password.css (3 files)
3. **`.stat-card`** - Identical definitions in: dashboard.css, appointments.css, imaging.css, medical-records.css, patients.css, reports.css, ai-insights.css (7 files + variations)
4. **`.form-group`** - Defined in multiple CSS files
5. **Table wrapper + table** - Defined 5+ times (appointment, patient, imaging, activity, report)
6. **Search input styles** - Defined in multiple module CSS files

---

### HARD-CODED COLORS (Should use design tokens)

1. `#e5bcbc` - Error border (should use --cm-danger or variant)
2. `#fff5f5` - Error background (should use --cm-danger-soft)
3. `#b42318` - Error text (should use --cm-danger)
4. `#fff4d6` - Warning background (should use --cm-warning-soft)
5. `#9a6700` - Warning text (should use --cm-warning)
6. `#f1f1f1` - Inactive background (should use --cm-surface-muted)
7. `#666` - Inactive text (should use --cm-text-muted)
8. Various email template colors in HTML inline styles

---

### INLINE STYLES FOUND

1. `templates/patients.html` line 290: `style="text-align: center;"` - Should use utility class
2. Email templates use inline `<style>` with hard-coded colors

---

### JAVASCRIPT SELECTOR DEPENDENCIES

The following CSS classes are used by JavaScript and MUST NOT be renamed without updating JS:

- `.sidebar-link` - Navigation active state management
- `.sidebar` - Mobile menu toggle
- `.mobile-menu-button` - Mobile menu trigger
- `.notification-button` - Notification click handler
- `.navbar-toggle` - Navbar toggle (in app.js)
- `.navbar-menu` - Navbar menu (in app.js)
- `.message-close` - Message dismissal (in app.js)
- `.navbar-menu a` - Menu link navigation (in app.js)
- `.sidebar` - Sidebar scroll lock (in app.js)

---

## SUMMARY: COMPONENT ARCHITECTURE ISSUES

### Critical Issues (Must Fix)
1. ❌ **Button system fragmented** across 4 CSS files - need unified system
2. ❌ **Stat card component duplicated** 7+ times - massive code duplication
3. ❌ **Table component duplicated** 5+ times - maintenance burden
4. ❌ **Hard-coded colors** throughout (errors, warnings) - breaks design system
5. ❌ **Form inputs inconsistent** (padding, background color variations)
6. ❌ **No modal/dropdown** components
7. ❌ **No loading/empty states** standardized

### High Priority
1. 🟡 **Mobile search inputs** fixed width - not responsive
2. 🟡 **No AI visual language** - AI components lack distinctiveness
3. 🟡 **Accessibility gaps** - missing ARIA, color-only indicators
4. 🟡 **Mixed naming conventions** (.primary-button vs .button.button-primary)
5. 🟡 **No focus states** on most components beyond global :focus-visible

### Medium Priority
1. 🟠 **No toast notifications** - only page-level messages
2. 🟠 **No breadcrumbs** - navigation clarity
3. 🟠 **No tabs** - accordion-only for tabbed content
4. 🟠 **No pagination** - not visually defined
5. 🟠 **Icon system unclear** - mix of emoji, Unicode, potential SVG

### Low Priority (Polish)
1. 🟡 Micro-interactions minimal
2. 🟡 Loading animations not defined
3. 🟡 Disabled state inconsistent
4. 🟡 Hover transitions could be smoother

---

## RECOMMENDED COMPONENT ARCHITECTURE

```
templates/components/
├── buttons/
│   ├── button.html (unified button component)
│   └── icon_button.html
├── cards/
│   ├── card.html (base card)
│   ├── stat_card.html
│   ├── appointment_card.html
│   ├── patient_card.html
│   └── ai_insight_card.html
├── forms/
│   ├── form_field.html
│   ├── form_group.html
│   ├── text_input.html
│   ├── select.html
│   ├── checkbox.html
│   ├── radio.html
│   └── form_error.html
├── alerts/
│   ├── alert.html (info/success/warning/danger)
│   └── inline_error.html
├── badges/
│   ├── badge.html (base)
│   ├── status_badge.html
│   └── notification_badge.html
├── tables/
│   ├── table.html
│   └── table_row_actions.html
├── navigation/
│   ├── breadcrumbs.html
│   ├── pagination.html
│   ├── tabs.html
│   └── dropdown.html
├── modals/
│   └── modal.html
├── notifications/
│   ├── notification_item.html
│   └── notification_list.html
├── ai/
│   ├── ai_badge.html
│   ├── ai_insight_card.html
│   └── ai_recommendation.html
├── states/
│   ├── empty_state.html
│   ├── loading_skeleton.html
│   └── error_state.html
├── footer.html (existing)
├── messages.html (existing)
├── navbar.html (existing)
└── sidebar.html (existing)

static/css/
├── base.css (design tokens - COMPLETE)
├── layout.css (app shell - NO CHANGE)
├── components.css (NO CHANGE - will add new components)
├── components/
│   ├── buttons.css (unified button system)
│   ├── cards.css (unified card system)
│   ├── forms.css (unified form system)
│   ├── alerts.css (alert/notification system)
│   ├── badges.css (badge system)
│   ├── tables.css (table system)
│   ├── navigation.css (nav components)
│   ├── modals.css (modal system)
│   ├── ai.css (AI-specific components)
│   ├── states.css (empty/loading/error)
│   └── accessibility.css (a11y enhancements)
└── [module-specific CSS - REDUCED]

static/js/
├── components/ (NEW)
│   ├── dropdown.js
│   ├── modal.js
│   ├── notification.js
│   └── tabs.js
├── main.js (existing)
├── app.js (existing)
└── sidebar.js (existing)
```

---

## NEXT STEPS

✅ **STEP 1 COMPLETE:** Full audit without modifications  
⏳ **STEP 2:** Create component architecture based on this audit  
⏳ **STEP 3:** Implement unified button system  
⏳ **STEP 4:** Implement unified card system  
⏳ **STEP 5:** Implement unified form system  
⏳ **Remaining:** Alerts, badges, tables, navigation, modals, AI components, states  

---

**Audit completed:** All findings documented  
**No files modified** during audit  
**Ready to proceed to STEP 2**
