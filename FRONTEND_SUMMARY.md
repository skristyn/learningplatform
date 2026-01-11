# Frontend Application Summary
## Vue.js Learning Platform

---

## Architecture Overview

**Tech Stack:**
- **Vue 3** (Composition API + Options API)
- **Vue Router 4** (Hash-based routing)
- **Vuex 4** (Centralized state management)
- **TypeScript** (Full type safety)
- **Sass/SCSS** (Styling)
- **Floating Vue** (Dropdown components)
- **PWA** (Service Worker enabled)

**Build Output:**
- Production: `dist/production/`
- Development: `dist/development/`

---

## Application Structure

```
frontend/src/
├── views/           # Page components (Login, Home, CourseDashboard, Lesson, etc.)
├── components/      # Reusable UI components (DTabs, DButton, LessonSlide, etc.)
├── layouts/         # Layout wrappers (MainLayout, LessonLayout)
├── router/          # Route configuration and auth guards
├── store/           # Vuex store - centralized state
├── types/           # TypeScript interfaces (User, Lesson, Section, etc.)
├── utils/           # API utilities (getRequest, postRequest, getToken)
└── assets/          # Images and SVG files
```

---

## Routing & Navigation

### Main Routes

| Path | Component | Purpose | Auth Required |
|------|-----------|---------|---------------|
| `/login` | Login.vue | Authentication | Guest only |
| `/` | Home.vue | Landing page with "continue" button | Yes |
| `/course-dashboard` | CourseDashboard.vue | Course overview with progress | Yes |
| `/lesson-intro/:lessonId/:sectionId` | LessonIntro.vue | Pre-lesson introduction | Yes |
| `/lesson/:lessonId/:sectionId` | Lesson.vue | Main learning experience | Yes |
| `/sandbox` | Sandbox.vue | Testing/development | Yes |

### Authentication Guards

- Routes check `store.state.isAuthenticated`
- Unauthenticated users → redirect to `/login`
- Authenticated users on `/login` → redirect to `/`

---

## State Management (Vuex Store)

### State Structure

```typescript
{
  authToken: string | null              // JWT token from API
  isAuthenticated: boolean               // Auth status flag
  user: User | null                      // Current user profile
  userProgress: UserProgress | null      // Learning progress data
  textbook: Textbook | null              // Full course structure
  currentLesson: Lesson | null           // Active lesson
  currentSection: Section | null         // Active section with slides
  currentSlide: string | null            // Current slide ID
  currentImage: SlideImage | null        // Image for current slide
  currentTips: Tip[]                     // Tips for current slide
  alerts: Alert[]                        // UI notifications
}
```

### Key Actions

**Authentication:**
- `logIn({username, password})` → POST `/api/v1/token-auth`
- `logInWithToken(token)` → Restore session from localStorage
- `logOut()` → Clear token and redirect

**Data Loading:**
- `getUser()` → GET `/whoami` - User profile
- `getUserProgress()` → GET `/home` - Progress data
- `getDigitalStewardTextbook()` → GET `/textbooks/4/` - Full course
- `getCurrentLesson(id)` → GET `/lessons/{id}/` - Lesson with sections
- `getCurrentSection(id)` → GET `/sections/{id}/` - Section with slides
- `getCurrentImage(id)` → GET `/images/{id}/` - Slide image
- `getCurrentTips(slideId)` → GET `/tips/?slide_id={id}` - Tips list

**User Interactions:**
- `updateTips(body)` → POST `/tips/` - Submit new tip
- `markSectionComplete()` → POST `/grades/` - Record completion

---

## API Integration

### API Module (`utils/api.ts`)

```typescript
// GET requests with auth token
getRequest<T>(path: string, token: string): Promise<T>

// POST requests with auth token
postRequest<T>(path: string, body: object, token: string): Promise<T>

// Login to get auth token
getToken(username: string, password: string): Promise<{token: string}>
```

### All API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/token-auth` | POST | Get authentication token |
| `/whoami` | GET | Get current user info |
| `/home` | GET | Get user progress & announcements |
| `/textbooks/4/` | GET | Get complete course structure |
| `/lessons/{id}/` | GET | Get lesson with nested sections |
| `/sections/{id}/` | GET | Get section with all slides |
| `/images/{id}/` | GET | Get slide image metadata |
| `/tips/?slide_id={id}` | GET | Get tips for a slide |
| `/tips/` | POST | Submit new tip |
| `/grades/` | POST | Mark section complete |

### Authentication Flow

1. User submits login form
2. `getToken()` calls `/token-auth` with credentials
3. Backend returns `{token: "abc123..."}`
4. Token stored in:
   - `state.authToken`
   - `localStorage.setItem('token', token)`
5. All subsequent requests include header:
   ```
   Authorization: Token abc123...
   ```

---

## Key Views/Pages

### Login.vue
- Simple username/password form
- Calls `store.dispatch('logIn')`
- Redirects to Home on success
- Displays error alerts from store

### Home.vue
- Landing page after login
- Fetches `getUserProgress` on mount
- Shows announcement banner if available
- **"Continue where you left off"** button
- Links to Course Overview and Resource Kit

### CourseDashboard.vue
- Full course overview page
- Loads entire textbook structure
- Features:
  - **Progress bar** (% of sections completed)
  - **Tabbed interface** (Lessons, Resources, Project)
  - **LessonList** - Expandable lessons showing sections
  - **Quick continue button** to next incomplete section
  - **Announcement banner**
- Calculates progress from completed sections

### LessonIntro.vue
- Pre-lesson introduction screen
- Shows:
  - Breadcrumb navigation
  - Section title and description
  - Estimated time to complete
  - "Begin Lesson!" button
- Links to main Lesson view

### Lesson.vue
- **Main learning experience** - slide-by-slide content
- Two-column layout:
  - **Left:** LessonSlide component (content display)
  - **Right:** LessonSidebar (Notes/Tips, collapsible)
- Features:
  - **Slide navigation** (Previous/Next buttons)
  - **Progress dots** (click to jump to slide)
  - **Slide content** with 3 layout types
  - **Tips sidebar** (view/share tips)
  - **Notes sidebar** (personal notes)
  - **Mark complete** button on last slide

---

## Core Components

### Layout Components

**MainLayout.vue**
- Standard page layout with SiteHeader
- Used for: Login, Home, CourseDashboard, LessonIntro

**LessonLayout.vue**
- Two-column layout for learning experience
- Left: LessonSidebar (collapsible)
- Right: Main lesson content
- Used for: Lesson.vue

### Learning Components

**LessonSlide.vue** - Displays slide content
- Props: slide, slideIndex, image
- Supports 3 slide layouts:
  - `headlineleftimage` - Image left, text right with heading
  - `imagerightblock` - Text left, image right
  - `imagetopblock` - Image top, text bottom
- Renders HTML body content with `v-html`
- Shows "Mark lesson complete" on last slide

**LessonFooter.vue** - Navigation and progress
- Previous/Next navigation buttons
- Progress dots showing all slides
- Clickable dots to jump to specific slide
- Star icon on last slide dot

**LessonSidebar.vue** - Collapsible sidebar
- Toggle between Notes and Tips views
- Collapse/expand button
- Shows lesson.number and section.title
- Exit Lesson button

**Tips.vue** - Tips sharing panel
- Three views: Display, Share, Thank you
- Lists existing tips for current slide
- Form to submit new tips
- Dispatches `updateTips` action

**Notes.vue** - Note-taking panel
- Add/view personal notes
- Textarea for input
- Local state only (persistence TODO)

### List Components

**LessonList.vue** - Lists all lessons
- Expandable lesson groups (DExpandable)
- Shows completion status
- First incomplete lesson auto-expanded
- Contains SectionList for each lesson

**SectionList.vue** - Lists sections in lesson
- Links to LessonIntro route
- Shows completion checkmarks
- Time estimates displayed
- Format: "Section 1.1: Title"

### UI Components

**DButton.vue** - Styled button/link
- Pink border with shadow styling
- Works as router-link

**DTabs.vue** - Tab navigation
- Icon + label for each tab
- Green highlight on selection

**DProgressBar.vue** - Visual progress bar
- Teal colored bar
- Shows percentage complete

**DExpandable.vue** - Collapsible section
- Used in LessonList
- Chevron toggle icon

**DPageHeader.vue** - Page header wrapper
**DBreadcrumb.vue** - Navigation breadcrumb
**DPageTitle.vue** - Large title display

---

## User Flow

### Complete Learning Journey

```
1. LOGIN
   └─ Enter credentials → Get auth token → Store in localStorage → Redirect to Home

2. HOME PAGE
   └─ Load getUserProgress → Show announcement
   └─ Display "Continue where you left off" button
   └─ Link to Course Overview

3. COURSE OVERVIEW
   └─ Load getDigitalStewardTextbook (full structure)
   └─ Display lessons with expandable sections
   └─ Show progress bar (% complete)
   └─ Quick continue button to next incomplete section

4. LESSON INTRODUCTION
   └─ Show section description & time estimate
   └─ Click "Begin Lesson!" → Route to Lesson view

5. MAIN LESSON EXPERIENCE
   ├─ Load getCurrentSection (all slides)
   ├─ Display first slide
   │
   ├─ FOR EACH SLIDE:
   │  ├─ Fetch getCurrentImage (if slide has image)
   │  ├─ Fetch getCurrentTips (tips for this slide)
   │  ├─ Display content based on layout type
   │  └─ Show tips/notes in sidebar
   │
   ├─ NAVIGATION:
   │  ├─ Click Previous/Next buttons
   │  ├─ Click progress dots to jump
   │  └─ Fade transition between slides
   │
   └─ ON LAST SLIDE:
      ├─ Show "Mark lesson complete" button
      ├─ Click → dispatch markSectionComplete()
      ├─ POST to /grades/ endpoint
      └─ Section marked complete in database

6. PROGRESS TRACKING
   └─ CourseDashboard updates with new completion status
   └─ Next incomplete section becomes new "continue" target
```

### Slide Types & Layouts

**Three slide layout types:**

1. **headlineleftimage**
   - Heading across top
   - Image on left side
   - Body text on right side

2. **imagerightblock**
   - Body text on left side
   - Image on right side

3. **imagetopblock**
   - Image across top
   - Body text below

**Slide Data Structure:**
```typescript
{
  type: "headlineleftimage" | "imagerightblock" | "imagetopblock"
  value: {
    heading: string       // Optional heading text
    body: string         // HTML body content
    image: number        // Image ID (fetched separately)
  }
  id: string            // Unique slide identifier
  tips_url: string      // URL to fetch tips
}
```

---

## Data Models (TypeScript)

### User & Progress

```typescript
interface User {
  id: number
  username: string
  profile_complete: boolean
  pronouns: string
}

interface UserProgress {
  current_user: {username, id}
  current_course: {title, detail_url}
  current_lesson: {title, lesson_num, detail_url}
  next_section: {title, section_num, detail_url}
  announcement: string
}
```

### Course Structure

```typescript
interface Textbook {
  id: number
  title: string
  description: string
  lessons: TextbookLesson[]
  completed: boolean
}

interface TextbookLesson {
  id: number
  lesson_num: number
  title: string
  completed: boolean
  time_remaining: number
  sections: TextbookSection[]
}

interface TextbookSection {
  id: number
  title: string
  description: string
  completed: boolean
  section_num: number
  time_to_complete: number
}

interface Section {
  id: number
  title: string
  description: string
  slides: Slide[]
  completed: boolean
  time_to_complete: number
}
```

### Content Types

```typescript
interface Slide {
  type: string
  value: {heading, body, image}
  id: string
  tips_url: string
}

interface SlideImage {
  id: number
  title: string
  meta: {
    download_url: string  // Full image URL
  }
}

interface Tip {
  user?: string
  body: string
  created_at?: string
}
```

---

## Key Features

### ✅ Implemented

1. **Token-based authentication** with session persistence (localStorage)
2. **Hierarchical course structure** (Textbooks → Lessons → Sections → Slides)
3. **Progress tracking** at section level
4. **Visual progress indicators** (progress bar, checkmarks, completion status)
5. **Three flexible slide layouts** (image positioning options)
6. **Tips sharing** (user-generated content per slide)
7. **Notes taking** (personal notes per section)
8. **Collapsible sidebar** for distraction-free learning
9. **Responsive navigation** (Previous/Next, jump to slide)
10. **Announcement system** (admin-to-student messaging)
11. **Type-safe codebase** (full TypeScript)
12. **PWA support** (offline capability with service worker)

### 🚧 TODOs (From Code Comments)

1. Notes persistence to backend not implemented
2. Generic textbook loading (currently hardcoded to textbook ID 4)
3. Loading states and error handling improvements
4. Resources tab not populated
5. Project tab not populated
6. Input sanitization for user-submitted content
7. Mobile responsiveness optimization
8. Chat/messaging features (commented out)

---

## Environment Configuration

### Environment Variables

- `VUE_APP_API_URL` - Base URL for all API calls
  - Development: `http://localhost:8000`
  - Production: Set in `.env.production`

### Build Commands

```bash
npm run serve-dev        # Dev server with hot reload
npm run serve            # Production mode dev server
npm run build            # Production build → dist/production/
npm run build-dev        # Development build → dist/development/
npm run lint             # ESLint validation
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Vue 3 Frontend                         │
│                                                             │
│  ┌──────────────┐          ┌──────────────┐               │
│  │   Router     │◄────────►│   Vuex Store │               │
│  │  (Routes &   │          │  (State Mgmt)│               │
│  │   Guards)    │          └──────┬───────┘               │
│  └──────┬───────┘                 │                        │
│         │                         │                        │
│         │                         │                        │
│         ▼                         ▼                        │
│  ┌──────────────────────────────────────────────┐         │
│  │           Views & Components                 │         │
│  │  (Login, Home, Dashboard, Lesson, etc.)      │         │
│  └──────────────────────────────────────────────┘         │
│                         │                                  │
│                         ▼                                  │
│                  ┌──────────────┐                          │
│                  │ API Utilities│                          │
│                  │(HTTP Layer)  │                          │
│                  └──────┬───────┘                          │
└─────────────────────────┼──────────────────────────────────┘
                          │
                          │ REST API Calls
                          │ (Authorization: Token)
                          ▼
               ┌────────────────────┐
               │   Django Backend   │
               │   (API Endpoints)  │
               └────────────────────┘
```

---

## Component Hierarchy

```
App.vue
│
├─ MainLayout (most pages)
│  ├─ SiteHeader (with profile dropdown)
│  └─ Router View
│     ├─ Login
│     ├─ Home
│     ├─ CourseDashboard
│     │  ├─ DPageHeader
│     │  ├─ DTabs
│     │  ├─ DProgressBar
│     │  └─ LessonList
│     │     └─ DExpandable
│     │        └─ SectionList
│     └─ LessonIntro
│
└─ LessonLayout (lesson pages)
   ├─ LessonSidebar
   │  ├─ Notes
   │  └─ Tips
   └─ Router View
      └─ Lesson
         ├─ LessonSlide
         └─ LessonFooter
```

---

## Security & Best Practices

**Authentication:**
- JWT tokens stored in localStorage
- Token sent in Authorization header on every request
- Auth guards prevent unauthorized access

**Type Safety:**
- Full TypeScript coverage
- Interfaces for all data models
- Type-safe API calls

**Code Organization:**
- Clear separation of concerns
- Reusable components
- Centralized state management
- Consistent naming conventions

**Performance:**
- Lazy-loaded routes (code splitting)
- Service worker (PWA)
- Image caching

---

## Deployment

**Production Build:**
```bash
cd frontend
npm run build                    # Builds to dist/production/
```

**Static Files Location (After Build):**
```
dist/production/
├── index.html
├── css/
├── js/
└── img/
```

**Served By:**
- Nginx serves static files from `/staticfiles/frontend/`
- API requests proxied to Django backend

**URL Structure:**
- Frontend: All routes handled by Vue Router (/#/route)
- API: `/api/v1/*` proxied to Django
- Admin: `/admin/` and `/django-admin/` proxied to Django

---

## Summary

This Vue 3 frontend provides a complete learning management experience with:

- **User authentication** and session management
- **Hierarchical course structure** (textbooks, lessons, sections, slides)
- **Progress tracking** and visual indicators
- **Interactive learning** with slides, images, tips, and notes
- **Clean architecture** with TypeScript, Vuex, and Vue Router
- **Responsive design** with collapsible layouts
- **API-first approach** connecting to Django REST backend

The application follows Vue best practices with component-based architecture, centralized state management, type safety, and clear separation between UI logic and data fetching.
