<template>
  <div>
    <CardTitle>Information</CardTitle>
    <CardContent class="grid grid-cols-12 gap-12">
      <div class="col-span-4 md:col-span-2">
        <ProfilePicture class="cursor-pointer" :user="member" size="xl" />
      </div>
      <div class="col-span-8 md:col-span-4">
        <Input
          ref="member-first-name"
          v-model:value="member.first_name"
          label="First Name"
          type="text"
          placeholder="First Name"
          :disabled="member.id !== currentUser.id"
        />
        <Input
          ref="member-last-name"
          v-model:value="member.last_name"
          class="mt-2"
          label="Last Name"
          type="text"
          placeholder="Last Name"
          :disabled="member.id !== currentUser.id"
        />
        <Input
          ref="member-email"
          v-model:value="member.email"
          class="mt-2"
          label="Email"
          type="email"
          placeholder="Email"
          :disabled="member.id !== currentUser.id"
        />
        <Select
          ref="member-role"
          v-model:value="member.member_type"
          class="mt-2"
          label="Role"
          placeholder="Role"
          :options="optionsRole"
        />
        <Button class="mt-4 w-full" type="primary" @click="updateUser">
          Save
        </Button>
      </div>
    </CardContent>
  </div>
</template>

<script>
import { ref, computed } from "vue";
import { useStore } from "vuex";

import Button from "@/components/Button.vue";
import Input from "@/components/Input.vue";
import Select from "@/components/Select.vue";

import CardContent from "@/components/app/CardContent.vue";
import CardTitle from "@/components/app/CardTitle.vue";
import ProfilePicture from "@/components/app/ProfilePicture.vue";

import { MEMBER_GETTER_DETAILS, USER_GETTER_CURRENT } from "@/store/types";

export default {
  components: {
    Button,
    Input,
    Select,

    CardContent,
    CardTitle,
    ProfilePicture,
  },
  props: {
    userId: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const store = useStore();

    const currentUser = computed(() => store.getters[USER_GETTER_CURRENT]);

    const user = computed(() => {
      if (props.userId === currentUser.value.id) {
        return store.getters[USER_GETTER_CURRENT];
      }
      return store.getters[MEMBER_GETTER_DETAILS](props.userId);
    });
    const member = ref({ ...user.value });

    // TODO: change roles based on current user's role
    // (only owners can assign other owners)
    const optionsRole = [
      { value: "owner", label: "Owner" },
      { value: "admin", label: "Admin" },
      { value: "developer", label: "Developer" },
      { value: "translator", label: "Translator" },
    ];

    function updateUser() {}

    return {
      member,
      currentUser,
      optionsRole,

      updateUser,
    };
  },
};
</script>
