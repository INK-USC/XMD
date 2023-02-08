<template>
    <el-row>
      <!-- <el-col>
        <el-form>
            <el-form-item>
                <el-radio-group v-model="modelRadio">
                    <el-radio label="Model List" border @click="getModelList()"/>
                    <el-radio label="Upload Model" border/>
                </el-radio-group>
            </el-form-item>
        </el-form>
      </el-col>   -->
      <el-col>
        <el-card v-if="modelRadio == 'Model List'">
          <template #header>
            <h3>Model List
              <el-popover content="help text" trigger="hover" :width="400">
                <template #reference>
                  <el-icon style="height: 100%; margin-left: 0.5rem">
                    <QuestionFilled />
                  </el-icon>
                </template>
              </el-popover>
            </h3>
          </template>

        <el-table
        :data="this.modelList"
        stripe
        style="width: 100%"
        >
            <el-table-column prop="id" label="Id"/>
            <el-table-column prop="name" label="Name"/>
            <el-table-column prop="model" label="Model path"/>
            <el-table-column prop="uploaded_at" label="Uploaded at"/>
        </el-table>

        </el-card>
        <el-card v-if="modelRadio == 'Upload Model'">
          <template #header>
            <h3>Upload new model <span style="color: #909399">(Optional)</span></h3>
          </template>

          
          <el-form :model="this.fileForm" ref="modelUploadForm" style="text-align: center">
            <el-form-item>
              <el-radio v-model="fileForm.fileType" label=".zip" border>.ZIP file</el-radio>
            </el-form-item>
            <el-form-item>
              <el-upload
                v-model:file-list="fileForm.fileZip"
                drag
                accept=".zip"
                ref="uploadInput"
                action=""
                :http-request="handleUpload"
              >
                <el-icon :size="48"><UploadFilled /></el-icon>
                <div class="el-upload__text">
                  Drop file here or <em>click to upload</em>
                </div>
              </el-upload>
            </el-form-item>

            <div class="success" style="color: green;" v-if="savingSuccessful"> 
                <p>Model was saved successfully <el-icon><SuccessFilled /></el-icon></p>
            </div>

          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </template>
  
  <script>
  import { UploadFilled, Upload, SuccessFilled, QuestionFilled } from "@element-plus/icons-vue";
  import { useProjectStore } from "@/stores/project";
  import ModelsApi from "@/utilities/network/model";
  
  // show user the correct format of their document to upload. and allow them to upload doc
  export default {
    name: "ModelUpload",
    components: {
      UploadFilled,
      Upload,
      SuccessFilled,
      QuestionFilled
    },
    setup() {
      const projectStore = useProjectStore();
      return {
        projectStore,
      };
    },
    data() {
      return {
        modelRadio: 'Upload Model',
        modelList: [],

        fileForm: {
          fileType: ".zip",
          fileZip: [],
          file: null,
        },

        savingSuccessful: false,
      };
    },
    methods: {
    //   handleChange(uploadFile, uploadFiles) {
    //     console.log(this.$refs.uploadInput)
    //     this.fileForm.file = this.$refs.uploadInput.files[0];
    //   }, 
      handleUpload(param) {
        // console.log(`from param var: ${param.file}`);
        // console.log(`from data var: ${this.fileForm.fileZip[0]}`);
        // this.fileForm.fileZip[-1] = param.file;
        // this.fileForm.file = param.file
        ModelsApi.uploadModel(
        this.projectStore.getProjectInfo.id,
        param.file,
        // this.fileForm.name,
        // this.fileForm.description,
        this.fileForm.fileType
        )
        .then((res) => {
            console.log(res);
            if (res?.success) {
                this.savingSuccessful=true;
            }
            // this.$router.push({ name: "Labels" });
        })
        .catch((err) => {
            console.log(err);
        });
      },
      uploadFile() {
        this.$refs['modelUploadForm'].validate((isValid) => {
            if (isValid) {
                ModelsApi.uploadModel(
                this.projectStore.getProjectInfo.id,
                this.fileForm.file,
                // this.fileForm.name,
                this.fileForm.description,
                this.fileForm.fileType
                )
                .then(() => {
                    // this.$router.push({ name: "Labels" });
                })
                .catch((err) => {
                    console.log(err);
                });
            }
        })
      },
      getModelList() {
        ModelsApi.list(this.projectStore.getProjectInfo.id)
        .then((res) => {
            this.modelList = res.results;
            console.log('res', res);
            console.log('model list:', this.modelList);
        });
      },
      created() {
        this.getModelList();
      }
    },
  };
  </script>
  
  <style scoped>
  pre {
    background-color: rgb(245, 245, 245);
  }
  </style>
  