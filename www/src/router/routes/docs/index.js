const routes = [
  {
    path: "/docs",
    name: "Docs",
    component: () => import("@/layouts/Docs.vue"),
    children: [
      {
        path: "/docs",
        name: "DocsHome",
        component: () => import("@/pages/docs/Home.vue"),
      },
      {
        path: "/docs/self-hosting",
        name: "SelfHost",
        component: () => import("@/pages/docs/SelfHost.vue"),
      },
    ],
  },
];

export default routes;
