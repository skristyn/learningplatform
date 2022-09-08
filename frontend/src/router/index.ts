import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import MainLayout from "@/layouts/MainLayout.vue";
import LessonLayout from "@/layouts/LessonLayout.vue";
import { BreadcrumbTrail } from "@/types/BreadcrumbTrail";
import store from "../store";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: { layout: MainLayout, guest: true }, // show signin page if logged out, otherwise show home page
  },
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: { layout: MainLayout, requiresAuth: true },
  },
  {
    path: "/course-dashboard",
    name: "CourseDashboard",
    // TODO decide if these should continue to be lazy loaded
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(
        /* webpackChunkName: "coursedashboard" */ "../views/CourseDashboard.vue"
      ),
    meta: { layout: MainLayout, requiresAuth: true },
  },
  {
    path: "/lesson-intro/:lessonId/:sectionId",
    name: "LessonIntro",
    component: () =>
      import(/* webpackChunkName: "lessonintro" */ "../views/LessonIntro.vue"),
    props: true,
    // TODO consider refactoring how the previous breadcrumb is set
    meta: {
      layout: MainLayout,
      requiresAuth: true,
      breadcrumbTrail: {
        routeName: "CourseDashboard",
        crumbTitle: "Digital Stewards Training",
      } as BreadcrumbTrail,
    },
  },
  {
    path: "/lesson/:lessonId/:sectionId",
    name: "Lesson",
    component: () =>
      import(/* webpackChunkName: "lesson" */ "../views/Lesson.vue"),
    props: true,
    meta: { layout: LessonLayout, requiresAuth: true },
  },
  {
    path: "/sandbox",
    name: "Sandbox",
    component: () =>
      import(/* webpackChunkName: "sandbox" */ "../views/Sandbox.vue"),
    meta: { layout: MainLayout, requiresAuth: true },
  },
  {
    path: "/sandbox/sub",
    name: "SandboxSub",
    component: () =>
      import(/* webpackChunkName: "sandbox" */ "../views/SandboxSub.vue"),
    meta: {
      layout: MainLayout,
      requiresAuth: true,
      breadcrumbTrail: {
        routeName: "Sandbox",
        crumbTitle: "Sandbox testing page",
      } as BreadcrumbTrail,
    },
    // {
    //   path: "/about",
    //   name: "About",
    //   component: () =>
    //     import(/* webpackChunkName: "about" */ "../views/About.vue"),
    //   meta: { layout: MainLayout, requiresAuth: true },
    // },
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// if the path's requiresAuth is true,
// and the user is not authenticated, and the path isn't the Login page,
// redirect to the Login page
router.beforeEach((to, from) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!store.state.isAuthenticated && to.name !== "Login") {
      return { name: "Login" };
    }
  }
});

// if the path is the login guest page,
// and the user is already authenticated,
// redirect to the Home page
router.beforeEach((to, from) => {
  if (to.matched.some((record) => record.meta.guest)) {
    if (store.state.isAuthenticated && to.name !== "Home") {
      return { name: "Home" };
    }
  }
});

export default router;
