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
        path: "/about",
        name: "About",
        component: () => import("@/pages/landing/About.vue"),
      },
    ],
  },
];

export default routes;
