import appRoutes from "@/router/routes/app";
import authRoutes from "@/router/routes/auth";
import docsRoutes from "@/router/routes/docs";
import landingRoutes from "@/router/routes/landing";

const routes = [
  ...appRoutes,
  ...authRoutes,
  ...docsRoutes,
  ...landingRoutes,
  {
    path: "/:pathMatch(.*)",
    name: "NotFound",
    component: () => import("@/pages/app/NotFound.vue"),
  },
];

export default routes;
