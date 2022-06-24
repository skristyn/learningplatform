import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import MainLayout from "@/layouts/MainLayout.vue";
import LessonLayout from "@/layouts/LessonLayout.vue";
import { IBreadcrumbTrail } from "@/types/BreadcrumbTrail";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    // TODO: show signin page if logged out, otherwise show home page
    name: "Login",
    component: Login,
    meta: { layout: MainLayout },
  },
  {
    path: "/home",
    // TODO: show signin page if logged out, otherwise show home page
    name: "Home",
    component: Home,
    meta: { layout: MainLayout },
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
    meta: { layout: MainLayout },
  },
  {
    path: "/lesson/", // TODO should this be training/lesson?.... at least needs `/:id` at end of route
    name: "Lesson",
    component: () =>
      import(/* webpackChunkName: "lesson" */ "../views/Lesson.vue"),
    meta: { layout: LessonLayout },
  },
  {
    path: "/sandbox",
    name: "Sandbox",
    component: () =>
      import(/* webpackChunkName: "sandbox" */ "../views/Sandbox.vue"),
    meta: {
      layout: MainLayout,
    },
  },
  {
    path: "/sandbox/sub",
    name: "SandboxSub",
    component: () =>
      import(/* webpackChunkName: "sandbox" */ "../views/SandboxSub.vue"),
    meta: {
      layout: MainLayout,
      breadcrumbTrail: {
        routeName: "Sandbox",
        crumbTitle: "Sandbox testing page",
      } as IBreadcrumbTrail,
    },
  },
  // {
  //   path: "/LessonIntro",
  //   name: "LessonIntro",
  //   component: () =>
  //     import(/* webpackChunkName: "sandbox" */ "../views/LessonIntro.vue"),
  // },

  // {
  //   path: "/coursedashboard",
  //   name: "CourseDashboard",
  //   component: () =>
  //     import(
  //       /* webpackChunkName: "coursedashboard" */ "../views/CourseDashboard.vue"
  //     ),
  //   meta: { layout: MainLayout },
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

export default router;
