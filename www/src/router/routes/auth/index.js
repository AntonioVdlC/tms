const routes = [
  {
    path: "/auth",
    name: "Auth",
    component: () => import("@/layouts/Auth.vue"),
    children: [
      {
        path: "/auth/login",
        name: "Login",
        component: () => import("@/pages/auth/Login.vue"),
      },
      {
        path: "/auth/callback",
        name: "AuthCallback",
        component: () => import("@/pages/auth/Callback.vue"),
      },
      {
        path: "/auth/logout",
        name: "Logout",
        component: () => import("@/pages/auth/Logout.vue"),
      },
    ],
  },
];

export default routes;
