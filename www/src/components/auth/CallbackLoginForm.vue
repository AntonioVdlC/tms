<script>
import { useRouter } from "vue-router";

export default {
  setup() {
    const router = useRouter();
    router.push("/app");

    return null;
  },
};
</script>
