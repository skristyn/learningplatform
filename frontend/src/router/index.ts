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
    path: "/lesson/", // TODO should this be training/lesson?.... at least needs `/:id` at end of route
    name: "Lesson",
    component: () =>
      import(/* webpackChunkName: "lesson" */ "../views/Lesson.vue"),
    meta: { layout: LessonLayout, requiresAuth: true },
  },
  {
    path: "/about",
    name: "About",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
    meta: { layout: MainLayout, requiresAuth: true },
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
  },
  // {
  //   path: "/LessonIntro",
  //   name: "LessonIntro",
  //   component: () =>
  //     import(/* webpackChunkName: "sandbox" */ "../views/LessonIntro.vue"),
  // },

  // {
  //   path: "/lessons",
  //   name: "lessons",
  //   component: () =>
  //     import(/* webpackChunkName: "sandbox" */ "../views/CourseDashboard.vue"),
  //   meta: { layout: MainLayout },
  // },
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
