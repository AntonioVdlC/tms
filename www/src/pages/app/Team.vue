<template>
  <div>
    <CardTitle>Invite Colleagues</CardTitle>
    <CardContent>
      <p>
        You can invite an unlimited numbers of colleagues to
        <HighlightText>{{
          currentOrganistion.organisation_name
        }}</HighlightText>
        .
      </p>
      <div class="mt-4">
        <div class="sm:flex sm:items-center">
          <Input
            ref="invitee-email"
            v-model:value="email"
            class="sm:flex-grow"
            label="Email"
            type="email"
            placeholder="Email"
          />
          <Select
            ref="invitee-role"
            v-model:value="selectedRole"
            class="mt-2 sm:mt-0 sm:ml-4 sm:w-1/3"
            label="Role"
            placeholder="Role"
            :options="optionsRole"
          />
        </div>
        <div class="sm:text-right">
          <Button
            class="mt-2 w-full sm:w-1/3"
            type="secondary"
            :disabled="!isFormValid"
            @click="addInviteeToList"
          >
            Add
          </Button>
        </div>

        <Error v-if="formErrorMessage" class="mt-2">{{
          formErrorMessage
        }}</Error>
      </div>

      <Space :size="6" />

      <ul class="w-full">
        <li
          v-for="invitee in invitees"
          :key="`invitee-${invitee.email}`"
          class="flex flex-wrap justify-between mb-2"
        >
          <span class="flex-grow">{{ invitee.email }}</span>
          <span class="sm:w-1/3 flex justify-between items-center">
            <span class="mr-2 sm:mr-0">
              {{
                optionsRole.find((option) => option.value === invitee.role)
                  .label
              }}
            </span>
            <XIcon
              class="h-3 inline cursor-pointer"
              tabindex="0"
              @click="removeInvitee(invitee)"
              @keyup.enter="removeInvitee(invitee)"
            />
          </span>
        </li>
      </ul>
      <Button
        v-show="invitees.length"
        class="mt-4 w-full"
        type="primary"
        :is-loading="sendingInvites"
        @click="sendInvites"
      >
        Send Invites
      </Button>
    </CardContent>

    <Space :size="8" />

    <!-- Members -->
    <CardTitle>Members</CardTitle>
    <CardContent>
      <ul class="w-full">
        <li class="grid grid-cols-12 gap-4 font-bold">
          <span class="col-span-3">Name</span>
          <span class="col-span-3">Email</span>
          <span class="col-span-2">Role</span>
          <span class="col-span-3">Projects</span>
          <span>Status</span>
        </li>
        <li
          v-for="member in members"
          :key="member._id"
          class="grid grid-cols-12 gap-4 h-12"
        >
          <span class="col-span-3 flex items-center">
            <ProfilePicture
              v-if="member.first_name + member.last_name"
              :user="member"
              size="s"
              class="cursor-pointer"
              tabindex="0"
              @click="goToProfile(member)"
              @keyup.up="goToProfile(member)"
            />
            <span class="ml-2">
              <span v-if="member.first_name + member.last_name">
                {{ member.first_name }}{{ " " }}{{ member.last_name }}
              </span>
              <span v-else>-</span>
            </span>
          </span>
          <span class="col-span-3 flex items-center">{{ member.email }}</span>
          <span class="col-span-2 flex items-center">{{ member.role }}</span>
          <span class="col-span-3"></span>
          <span class="flex items-center">{{ member.status }}</span>
        </li>
      </ul>
    </CardContent>
  </div>
</template>

<script>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
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

import { XIcon } from "@heroicons/vue/solid";

import CardContent from "@/components/app/CardContent.vue";
import CardTitle from "@/components/app/CardTitle.vue";
import HighlightText from "@/components/app/HighlightText.vue";
import ProfilePicture from "@/components/app/ProfilePicture.vue";

import Button from "@/components/Button.vue";
import Error from "@/components/Error.vue";
import Input from "@/components/Input.vue";
import Select from "@/components/Select.vue";
import Space from "@/components/Space.vue";

export default {
  components: {
    XIcon,

    CardContent,
    CardTitle,
    HighlightText,
    ProfilePicture,

    Button,
    Error,
    Input,
    Select,
    Space,
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

    const email = ref("");
    const selectedRole = ref("");
    const optionsRole = [
      { value: "admin", label: "Admin" },
      { value: "developer", label: "Developer" },
      { value: "translator", label: "Translator" },
    ];

    const formErrorMessage = ref("");
    const isFormValid = computed(() => email.value && selectedRole.value);

    const invitees = ref([]);

    function addInviteeToList() {
      formErrorMessage.value = "";

      if (!email.value || !selectedRole.value) {
        return;
      }
      if (
        invitees.value.some((invitee) => invitee.email === email.value) ||
        members.value.some((member) => member.email === email.value)
      ) {
        formErrorMessage.value =
          "The email you are trying to add already exists in this organisation.";
        return;
      }
      invitees.value.push({
        email: email.value,
        role: selectedRole.value,
      });

      email.value = "";
      selectedRole.value = "";
    }
    function removeInvitee(invitee) {
      const index = invitees.value.findIndex(
        (user) => user.email === invitee.email
      );

      if (index > -1) {
        invitees.value.splice(index, 1);
      }
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
          role:
            member.member_type === "owner"
              ? "Owner"
              : optionsRole.find((role) => role.value === member.member_type)
                  .label,
          status: member.is_deleted ? "Deactivated" : "Active",
        })),
        ...store.getters[MEMBER_GETTER_INVITES].map((member) => ({
          ...member,
          sort_key: member.last_name + member.first_name,
          role: optionsRole.find((role) => role.value === member.member_type)
            .label,
          status: "Invited",
        })),
      ].sort(alphabetically("sort_key"))
    );

    function goToProfile(member) {
      router.push(`/app/profile/${member._id}`);
    }

    return {
      currentOrganistion,
      email,
      selectedRole,
      optionsRole,
      formErrorMessage,
      isFormValid,
      addInviteeToList,
      removeInvitee,
      invitees,
      sendInvites,
      sendingInvites,

      loadingMembers,
      members,
      goToProfile,
    };
  },
};
</script>
