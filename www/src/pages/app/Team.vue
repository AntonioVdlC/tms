<template>
  <div>
    <CardTitle>Invite Colleagues</CardTitle>
    <CardContent>
      <p>
        You can invite an unlimited numbers of colleagues to
        <HighlightText>{{
          currentOrganistion.organisation_name
        }}</HighlightText>
      </p>
      <div>
        <Input
          ref="invitee-email"
          v-model:value="email"
          label="Email"
          type="email"
          placeholder="Email"
        />
        <Select
          ref="invitee-role"
          v-model:value="selectedRole"
          label="Role"
          placeholder="Role"
          :options="optionsRole"
        />
        <Button
          type="primary"
          :disabled="!isFormValid"
          @click="addInviteeToList"
        >
          Add
        </Button>
      </div>

      <ul>
        <li v-for="invitee in invitees" :key="`invitee-${invitee.email}`">
          <span>{{ invitee.email }}</span>
          <span>{{
            optionsRole.find((option) => option.value === invitee.role).label
          }}</span>
        </li>
      </ul>
      <Button
        v-show="invitees.length"
        type="primary"
        :is-loading="sendingInvites"
        @click="sendInvites"
      >
        Send Invites
      </Button>
    </CardContent>

    <!-- Members -->
    <CardTitle>Members</CardTitle>
    <CardContent>
      <ul class="w-full">
        <li class="grid grid-cols-12 font-bold">
          <span class="col-span-3">Name</span>
          <span class="col-span-3">Email</span>
          <span class="col-span-2">Role</span>
          <span class="col-span-3">Projects</span>
          <span>Status</span>
        </li>
        <li
          v-for="member in members"
          :key="member._id"
          class="grid grid-cols-12"
        >
          <span class="col-span-3 flex items-center">
            <ProfilePicture :user="member" size="s" />
            <span class="ml-2">
              {{ member.first_name }}{{ " " }}{{ member.last_name }}
            </span>
          </span>
          <span class="col-span-3">{{ member.email }}</span>
          <span class="col-span-2 flex items-center">{{
            member.member_type === "owner"
              ? "Owner"
              : optionsRole.find((role) => role.value === member.member_type)
                  .label
          }}</span>
          <span class="col-span-3"></span>
          <span class="flex items-center">{{ member.status }}</span>
        </li>
      </ul>
    </CardContent>
  </div>
</template>

<script>
import { computed, ref } from "vue";
import { useStore } from "vuex";

import { alphabetically } from "@/utils/sort-object";

import {
  MEMBER_ACTION_GET_LIST,
  MEMBER_ACTION_GET_INVITES,
  MEMBER_ACTION_CREATE,
  MEMBER_GETTER_LIST,
  MEMBER_GETTER_INVITES,
  ORGANISATION_GETTER_CURRENT,
  ORGANISATION_GETTER_LIST,
} from "@/store/types";

import CardContent from "@/components/app/CardContent.vue";
import CardTitle from "@/components/app/CardTitle.vue";
import HighlightText from "@/components/app/HighlightText.vue";
import ProfilePicture from "@/components/app/ProfilePicture.vue";

import Button from "@/components/Button.vue";
import Input from "@/components/Input.vue";
import Select from "@/components/Select.vue";

export default {
  components: {
    CardContent,
    CardTitle,
    HighlightText,
    ProfilePicture,

    Button,
    Input,
    Select,
  },
  setup() {
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

    const email = ref("");
    const selectedRole = ref("");
    const optionsRole = [
      { value: "admin", label: "Admin" },
      { value: "developer", label: "Developer" },
      { value: "translator", label: "Translator" },
    ];

    const isFormValid = computed(() => email.value && selectedRole.value);

    const invitees = ref([]);

    function addInviteeToList() {
      if (
        !email.value ||
        !selectedRole.value ||
        invitees.value.some((invitee) => invitee.email === email.value) ||
        members.value.some((member) => member.email === email.value)
      ) {
        return;
      }

      invitees.value.push({
        email: email.value,
        role: selectedRole.value,
      });

      email.value = "";
      selectedRole.value = "";
    }

    const sendingInvites = ref(false);
    function sendInvites() {
      sendingInvites.value = true;

      Promise.all(
        invitees.value.map((invitee) =>
          store.dispatch({
            type: MEMBER_ACTION_CREATE,
            payload: { email: invitee.email, member_type: invitee.role },
          })
        )
      ).finally(() => {
        invitees.value = [];
        sendingInvites.value = false;
      });
    }

    const loadingMembers = ref(true);
    Promise.all([
      store.dispatch({ type: MEMBER_ACTION_GET_LIST }),
      store.dispatch({ type: MEMBER_ACTION_GET_INVITES }),
    ]).finally(() => {
      loadingMembers.value = false;
    });
    const members = computed(() =>
      [
        ...store.getters[MEMBER_GETTER_LIST].map((member) => ({
          ...member,
          sort_key: member.last_name + member.first_name,
          status: member.is_deleted ? "Deactivated" : "Active",
        })),
        ...store.getters[MEMBER_GETTER_INVITES].map((member) => ({
          ...member,
          sort_key: member.last_name + member.first_name,
          status: "Invited",
        })),
      ].sort(alphabetically("sort_key"))
    );

    return {
      currentOrganistion,
      email,
      selectedRole,
      optionsRole,
      isFormValid,
      addInviteeToList,
      invitees,
      sendInvites,
      sendingInvites,

      loadingMembers,
      members,
    };
  },
};
</script>
