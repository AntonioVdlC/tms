const routes = [
  {
    path: "/app",
    name: "App",
    component: () => import("@/layouts/App.vue"),
    children: [
      {
        path: "/app",
        name: "Home",
        component: () => import("@/pages/app/Home.vue"),
      },
      {
        path: "/app/profile/:userId",
        props: true,
        name: "Profile",
        component: () => import("@/pages/app/Profile.vue"),
      },
      {
        path: "/app/team",
        name: "Team",
        component: () => import("@/pages/app/Team.vue"),
      },
      {
        path: "/app/projects",
        name: "Projects",
        component: () => import("@/pages/app/Projects.vue"),
      },
      {
        path: "/app/project/:projectId",
        props: true,
        name: "Project",
        component: () => import("@/pages/app/Project.vue"),
      },
      {
        path: "/app/project/:projectId/segment/:segmentId",
        props: true,
        name: "Segment",
        component: () => import("@/pages/app/Segment.vue"),
      },
      {
        path: "/app/reports",
        name: "Reports",
        component: () => import("@/pages/app/Reports.vue"),
      },
      {
        path: "/app/settings",
        name: "Settings",
        component: () => import("@/pages/app/Settings.vue"),
      },
      {
        path: "/app/billing",
        name: "Billing",
        component: () => import("@/pages/app/Billing.vue"),
      },
    ],
  },
];

export default routes;
