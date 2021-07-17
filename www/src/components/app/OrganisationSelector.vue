<template>
  <div>
    <Select
      v-model:value="selectedOrganisation"
      :options="optionsOrganisations"
    />
  </div>
</template>

<script>
import { ref, watch } from "vue";
import { useStore } from "vuex";

import {
  ORGANISATION_GETTER_CURRENT,
  ORGANISATION_ACTION_UPDATE_CURRENT,
} from "@/store/types";

import Select from "@/components/Select.vue";

export default {
  components: {
    Select,
  },
  props: {
    organisations: {
      type: Array,
      default: () => [],
    },
  },
  setup(props) {
    const store = useStore();

    const selectedOrganisation = ref(
      store.getters[ORGANISATION_GETTER_CURRENT]
    );
    watch(selectedOrganisation, (newValue) => {
      store.dispatch({
        type: ORGANISATION_ACTION_UPDATE_CURRENT,
        payload: { id: newValue },
      });
      // TODO: fetch all relevant data for the new organisation (projects, segments, members, ...)
    });

    const optionsOrganisations =
      props.organisations?.map((org) => ({
        value: org.id,
        label: org.organisation_name,
      })) ?? [];

    // TODO: implement a way to create new organisations, maybe in Settings?
    // optionsOrganisations.push({ value: "new", label: "Create" });

    return {
      selectedOrganisation,
      optionsOrganisations,
    };
  },
};
</script>
