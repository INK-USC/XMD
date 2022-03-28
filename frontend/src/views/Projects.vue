<template>
  <div>
    <div style="text-align: center">
      <h1>Hello, {{ this.userStore.username }}</h1>
      <el-row>
        <el-col :span="12" :offset="6">
          <el-button
            type="primary"
            @click="
              () => {
                this.selectedProject = null;
                this.dialogVisible = true;
              }
            "
            >CREATE PROJECT
          </el-button>
        </el-col>
      </el-row>
    </div>

    <el-row>
      <el-col :span="12" :offset="6">
        <el-table
          :data="projects"
          stripe
          :default-sort="{ prop: 'updated_at', order: 'descending' }"
        >
          <el-table-column prop="name" label="Name" sortable>
            <template #default="scope">
              <el-link
                type="primary"
                @click="handleProjectSelected(scope.$index, scope.row)"
              >
                {{ scope.row.name }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="Description" sortable />
          <el-table-column
            prop="task"
            label="Task"
            :formatter="convertTaskIDToString"
            sortable
            :filters="this.filters"
            :filter-method="filterTask"
          />
          <el-table-column
            prop="updated_at"
            label="Last Updated"
            :formatter="dateFormat"
            sortable
          />
          <el-table-column label="Operations">
            <template #default="scope">
              <el-button
                size="small"
                @click="handleEdit(scope.$index, scope.row)"
                ><el-icon><Edit /></el-icon>
                Edit
              </el-button>
              <el-popconfirm
                title="Are you sure?"
                @confirm="handleDelete(scope.$index, scope.row)"
                style="margin-left: 10px"
              >
                <template #reference>
                  <el-button size="small" type="danger"
                    ><el-icon><Delete /></el-icon>Delete</el-button
                  >
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
    <CreateProjectModal
      v-model:dialog-visible="dialogVisible"
      :existing-info="this.selectedProject"
    />
  </div>
</template>

<script>
import { DateTime } from "luxon";
import { Edit, Delete } from "@element-plus/icons-vue";

import CreateProjectModal from "@/components/project/CreateProjectModal.vue";
import { TaskTypes } from "@/utilities/constants";
import { useUserStore } from "@/stores/user";
import { useProjectStore } from "@/stores/project";
import ProjectsApi from "@/utilities/network/project";

// show all the project user create
export default {
  name: "ProjectsPage",
  components: {
    CreateProjectModal,
    Edit,
    Delete,
  },
  setup() {
    const userStore = useUserStore();
    const projectStore = useProjectStore();
    const filters = [];
    for (let item in TaskTypes) {
      filters.push({ text: TaskTypes[item], value: TaskTypes[item] });
    }
    return {
      userStore,
      projectStore,
      filters,
    };
  },
  data() {
    return {
      projects: [],
      dialogVisible: false,
      selectedProject: null,
    };
  },
  created: function () {
    this.fetchProjects();
  },
  methods: {
    handleProjectSelected(index, row) {
      this.$router.push({ name: "DocumentUpload" });
      this.projectStore.setProject(row);
    },
    handleEdit(index, row) {
      this.selectedProject = row;
      this.dialogVisible = true;
    },
    handleDelete(index, row) {
      ProjectsApi.list(row.id).then(() => {
        this.fetchProjects();
      });
    },
    fetchProjects() {
      ProjectsApi.list().then(
        (res) => {
          this.projects = res.results;
        },
        (err) => {
          console.log(err);
        }
      );
    },
    dateFormat(row, column) {
      let date = row[column.property];
      if (!date) {
        return "";
      }
      return DateTime.fromISO(date).toISODate();
    },
    convertTaskIDToString(row, column) {
      let taskId = row[column.property];
      if (!taskId) {
        return "";
      }
      return TaskTypes[taskId];
    },
    filterTask(value, row, column) {
      let taskId = row[column.property];
      let taskName = TaskTypes[taskId];
      return value === taskName;
    },
  },
};
</script>
