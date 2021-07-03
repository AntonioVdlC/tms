<template>
  <div>
    <CardTitle>Projects</CardTitle>
    <CardContent>
      <div class="sm:grid sm:grid-cols-3 sm:gap-4">
        <p class="sm:col-span-2">
          Projects allows you to better managed translation assignements and
          pipelines.
          <br />
          Your organisation
          <HighlightText>{{
            currentOrganistion.organisation_name
          }}</HighlightText>
          can have an <HighlightText>unlimited</HighlightText> number of
          projects.
        </p>
        <Button
          class="mt-2 w-full sm:mt-0 sm:self-center"
          type="primary"
          @click="goToCreateNewProject"
        >
          Create New Project
        </Button>
      </div>
    </CardContent>

    <ProjectList />
  </div>
</template>

<script>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import {
  ORGANISATION_GETTER_CURRENT,
  ORGANISATION_GETTER_LIST,
} from "@/store/types";

import Button from "@/components/Button.vue";
import CardContent from "@/components/app/CardContent.vue";
import CardTitle from "@/components/app/CardTitle.vue";
import HighlightText from "@/components/app/HighlightText.vue";
import ProjectList from "@/components/app/ProjectList.vue";

export default {
  components: {
    Button,
    CardContent,
    CardTitle,
    HighlightText,
    ProjectList,
  },
  setup() {
    const router = useRouter();
    const store = useStore();

    const selectedOrganisation = computed(
      () => store.getters[ORGANISATION_GETTER_CURRENT]
    );
    const organisations = computed(
      () => store.getters[ORGANISATION_GETTER_LIST]
    );

    const currentOrganistion = computed(() =>
      organisations.value.find((org) => org.id === selectedOrganisation.value)
    );

    function goToCreateNewProject() {
      router.push(`/app/projects/create`);
    }

    return {
      currentOrganistion,
      goToCreateNewProject,
    };
  },
};
</script>
