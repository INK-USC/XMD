<template>
  <el-row>
    <el-col>
      <el-card>
        <template #header>
          <h3>Import your corpus below</h3>
        </template>
        <div>
          <div>In order to start the annotation process, a corpus <u>must</u> be uploaded</div>
          <div>We accept datasets in the following formats:</div>
          <ul>
            <li>
              <b>JSON (recommended)</b>
              <br /><u>Format:</u>
              <pre
                style="
                  width: fit-content;
                  padding-left: 20px;
                  padding-right: 20px;
                  height: fit-content;
                "
              >
                <code>
                  {
                    "data" : [
                      {
                        "text" : "Louis Armstrong the great trumpet player lived in Corona.",
                      <template v-if="this.projectStore.task===1">
                        "label": "Label-Name-1"
                      </template><template v-if="this.projectStore.task===2">
                        "label": "Label-Name-1",
                        "start_offset": 0,
                        "end_offset": 5,
                      </template>
                      },
                      ...
                    ]
                  }
              </code>
							</pre>
              Each entry within <i>data</i> must have keys
              <i><b>text</b></i> and <i><b>words</b></i
              >. All other keys will be saved in a metadata dictionary
              associated with the text <br />
              The <i><b>annotations</b></i> key in each entry is optional. And,
              can be used to populate the document with label.
            </li>
          </ul>
          <div>Document Example: <a href="https://github.com/INK-USC/XMD/blob/master/annotation_backend/sample_data/tweeteval_hate_sample_100.json">[Dataset]</a></div>
          <br>
        </div>

        <el-form :model="this.fileForm" style="text-align: center">
          <el-form-item>
            <el-radio v-model="fileForm.fileType" label="JSON" border
              >JSON file</el-radio
            >
          </el-form-item>
          <el-form-item label="">
            <el-upload
              :http-request="uploadFile"
              drag
              accept="text/json"
              ref="uploadInput"
              action=""
            >
              <el-icon :size="48"><UploadFilled /></el-icon>
              <div class="el-upload__text">
                Drop file here or <em>click to upload</em>
              </div>
            </el-upload>
          </el-form-item>
        </el-form>
      </el-card>
    </el-col>
  </el-row>
  <UploadDocumentTutorial
    v-model:dialog-visible="tutorialVisible"
  />
</template>

<script>
import { UploadFilled } from "@element-plus/icons-vue";
import { useProjectStore } from "@/stores/project";
import DocumentsApi from "@/utilities/network/document";
import UploadDocumentTutorial from "@/components/project/tutorial/UploadDocumentTutorial.vue";

// show user the correct format of their document to upload. and allow them to upload doc
export default {
  name: "DocumentUpload",
  components: {
    UploadDocumentTutorial,
    UploadFilled,
  },
  setup() {
    const projectStore = useProjectStore();
    return {
      projectStore,
    };
  },
  data() {
    return {
      tutorialVisible: true,
      fileForm: {
        fileType: "JSON",
      },
    };
  },
  methods: {
    uploadFile(param) {
      DocumentsApi.uploadFile(
        this.projectStore.getProjectInfo.id,
        param.file,
        this.fileForm.fileType
      )
        .then(() => {
          this.$router.push({ name: "GenerateExplanations" });
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style scoped>
pre {
  background-color: rgb(245, 245, 245);
}
</style>
