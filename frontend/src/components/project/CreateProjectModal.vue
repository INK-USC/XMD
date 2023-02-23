<template>
  <el-dialog
    :title="this.existingInfo ? 'Edit Existing Project' : 'Create New Project'"
    v-model="dialogVisible"
    v-on:update:visible="$emit('update:dialogVisible', $event)"
    @open="this.dialogIsOpen"
    @close="$emit('update:dialogVisible', false)"
    width="40%"
  >
    <el-form :model="projectInfo" :rules="formRules" ref="projectInfoForm">
      <el-form-item label="Name" prop="name">
        <el-input v-model="projectInfo.name" />
      </el-form-item>
      <el-form-item label="Description" prop="description">
        <el-input v-model="projectInfo.description" />
      </el-form-item>
      <el-form-item label="Task" prop="task">
        <el-select
          remote
          v-model="projectInfo.task"
          placeholder="Select"
          style="width: 100%"
        >
          <el-option
            v-for="item in taskOptions"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="() => $emit('update:dialogVisible', false)"
          >Cancel</el-button
        >
        <el-button type="primary" @click="createProject">Confirm</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { TaskTypes } from "@/utilities/constants";
import { useProjectStore } from "@/stores/project";
import ProjectsApi from "@/utilities/network/project";

// the form when user create/edit a project
export default {
  name: "CreateProjectModal",
  props: { dialogVisible: Boolean, existingInfo: Object },
  setup() {
    const projectStore = useProjectStore();
    const taskOptions = [];
    for (let item in TaskTypes) {
      taskOptions.push({
        id: item,
        name: TaskTypes[item],
      });
    }
    return {
      projectStore,
      taskOptions,
    };
  },
  data() {
    return {
      projectInfo: {
        name: "",
        description: "",
        task: "",
      },
      formRules: {
        name: [
          {
            required: true,
            message: "Please input project name",
            trigger: "blur",
          },
        ],
        description: [
          {
            required: true,
            message: "Please input description",
            trigger: "blur",
          },
        ],
        task: [
          { required: true, message: "Please select task", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    dialogIsOpen() {
      if (this.existingInfo) {
        for (let key in this.existingInfo) {
          this.projectInfo[key] = this.existingInfo[key];
        }
      } else {
        this.projectInfo = {
          name: "",
          description: "",
          task: "",
        };
      }
    },
    // submit info to backend to create project if required parts are filled
    createProject() {
      this.$refs["projectInfoForm"].validate((isValid) => {
        if (isValid) {
          let httpRequest;
          if (this.existingInfo) {
            //edit
            httpRequest = ProjectsApi.update(this.projectInfo);
          } else {
            //create
            httpRequest = ProjectsApi.create(this.projectInfo);
          }
          httpRequest.then((res) => {
            this.projectStore.setProject(res);
            this.$emit("update:dialogVisible", false);
            this.$router.push({ name: "DocumentUpload" });
          });
        }
      });
    },
  },
};
</script>

<style scoped></style>
