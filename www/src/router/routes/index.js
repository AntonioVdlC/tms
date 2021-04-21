const routes = [
  {
    path: "/login",
    name: "Login",
    component: () => import("@/pages/Login.vue"),
  },
  {
    path: "/auth/callback",
    name: "AuthCallback",
    component: () => import("@/pages/AuthCallback.vue"),
  },
  {
    path: "/logout",
    name: "Logout",
    component: () => import("@/pages/Logout.vue"),
  },
  {
    path: "/",
    name: "Home",
    component: () => import("@/pages/Home.vue"),
  },
  {
    path: "/profile/:userId",
    props: true,
    name: "Profile",
    component: () => import("@/pages/Profile.vue"),
  },
  {
    path: "/team",
    name: "Team",
    component: () => import("@/pages/Team.vue"),
  },
  {
    path: "/projects",
    name: "Projects",
    component: () => import("@/pages/Projects.vue"),
  },
  {
    path: "/project/:projectId",
    props: true,
    name: "Project",
    component: () => import("@/pages/Project.vue"),
  },
  {
    path: "/project/:projectId/segment/:segmentId",
    props: true,
    name: "Segment",
    component: () => import("@/pages/Segment.vue"),
  },
  {
    path: "/reports",
    name: "Reports",
    component: () => import("@/pages/Reports.vue"),
  },
  {
    path: "/settings",
    name: "Settings",
    component: () => import("@/pages/Settings.vue"),
  },
  {
    path: "/billing",
    name: "Billing",
    component: () => import("@/pages/Billing.vue"),
  },
  {
    path: "/:pathMatch(.*)",
    name: "NotFound",
    component: () => import("@/pages/NotFound.vue"),
  },
];

export default routes;
