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
    ],
  },
];

export default routes;
