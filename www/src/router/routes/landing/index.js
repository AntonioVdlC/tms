const routes = [
  {
    path: "/",
    name: "Landing",
    component: () => import("@/layouts/Landing.vue"),
    children: [
      {
        path: "/",
        name: "LandingHome",
        component: () => import("@/pages/landing/Home.vue"),
      },
      {
        path: "/docs",
        name: "Docs",
        component: () => import("@/pages/landing/Docs.vue"),
      },
    ],
  },
];

export default routes;
