<template>
  <el-dialog
    v-model="dialogVisible"
    v-on:update:visible="$emit('update:dialogVisible', $event)"
    @close="$emit('update:dialogVisible', false)"
    width="50%"
  >
    <span slot="title" style="font-size: 18pt; font-weight:bold">Create Projects</span>
    <div class="container">
      <div class="row" style="padding: 10px">
          <br><br>
            <p class="text" style="font-size: 15pt; text-align: justify">
              Create a project to start with. <br>
              You can choose between sequence classification and relation extraction. <br>
              (Currently we only support sequence classification.)
            </p>
      </div>
    </div>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="() => $emit('update:dialogVisible', false)">
          Understand
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>

// the form when user create/edit a project
export default {
  name: "CreatePorjectTutorial",
  props: { dialogVisible: Boolean, existingInfo: Object },
  setup() {
  },
  data() {
    return {};
  },
  methods: {
  },
};
</script>

<style scoped></style>
