<template>
    <el-row style="width: 100%">
        <el-card style="width: 100%;">
            <template #header>
                <h3>Evaluation Section
                    <el-popover content="help text" trigger="hover" :width="400">
                        <template #reference>
                        <el-icon style="height: 100%; margin-left: 0.5rem">
                            <QuestionFilled />
                        </el-icon>
                        </template>
                    </el-popover>
                </h3>
            </template>
            <el-row>
                <span style="padding-right: 1em;">Model Selected: <b>{{model.model_name}}</b> </span>
                <el-button
                    type="primary"
                    size="small"
                    :loading="downloading"
                    @click="this.modelDownload()">
                    <el-icon>
                        <Download />
                    </el-icon>
                </el-button> 

                <el-divider />
                <h4>Example Input</h4>
                <el-form :model="exampleInputsForm" size="large" style="width: 100%">
                    <el-form-item>
                        <el-select v-model="exampleInputsForm.sentence_id" placeholder="Select a Sentence" size="large"
                            style="width: 100%;">
                            <el-option  
                                v-for="doc in documentStore.getDocuments"
                                :key="doc.id"
                                :label="doc.text"
                                :value="doc.id"
                            />
                        </el-select>
                    </el-form-item>

                </el-form>

                <div>
                    <h4 style="margin-top: 4em;">Attribution scores</h4>
                    <div>
                        <span><span
                                style="display: inline-block; width: 8em; text-align: left; font-style: italic;">Original</span>:
                            All muslims are terrorists and need to be deported from this country</span>
                    </div>
                    <div>
                        <span> <span
                                style="display: inline-block; width: 8rem; text-align: left; font-style: italic;">Debugged
                                Text</span>: All muslims are terrorists and need to be deported from this country</span>
                    </div>
                </div>

                <div v-if="exampleInputsForm.sentence_id !== ''">
                    <!-- test: {{ getDocText }} -->
                    {{ exampleInputsForm.sentence_id }}
                </div>
                


            </el-row>
        </el-card>
    </el-row>
</template>

<script>
import { Back, Check, Download } from "@element-plus/icons-vue";
import { useDocumentStore } from "@/stores/document";
import { useLabelStore } from "@/stores/label";
import { useDetailedDocumentStore } from "@/stores/detailedDocument";
import { useLocalDictionaryStore } from "@/stores/dictionaryLocal";
import { useProjectStore } from "@/stores/project";
import ModelsApi from "@/utilities/network/model";

export default {
    name: "DebugEvaluation",
    components: {
        Back,
        Check,
        Download
    },
    setup() {
        const documentStore = useDocumentStore();
        const detailedDocumentStore = useDetailedDocumentStore();
        const labelStore = useLabelStore();
        const localDictionaryStore = useLocalDictionaryStore();
        const projectStore = useProjectStore();
        return {
            documentStore,
            detailedDocumentStore,
            labelStore,
            localDictionaryStore,
            projectStore
        };
    },
    created() {
        const promises = [];
        promises.push(this.labelStore.fetchLabels());
        promises.push(
            this.documentStore.resetState().then(() => {
                return this.localDictionaryStore.fetchDictionary(
                    this.documentStore.getDocuments[
                        this.documentStore.getdocumentInfo.curDocIndex
                    ].id
                );
            })
        );
        Promise.all(promises).then(() => {
            this.detailedDocumentStore.fetchDocument(
                this.documentStore.getDocuments[
                    this.documentStore.getdocumentInfo.curDocIndex
                ].id
            );
        });
        this.getModelDetails()
    },
    data() {
        return {
            exampleInputsForm: {
                sentence_id: ""
            },
            downloading: false,
            model: {
                model_id: "",
                model_name: ""
            }
        }
    },
    computed: {
        getDocText() {
            console.log("calling getDocTest")
            console.log(this.exampleInputsForm.sentence_id)
            this.detailedDocumentStore.fetchDocument(this.exampleInputsForm.sentence_id)
            return this.detailedDocumentStore.getDocument
        }
    },
    methods: {
        getModelDetails() {
            ModelsApi.list(
                this.projectStore.getProjectInfo.id
            ).then(res => {
                console.log(res.results.at(-1));
                // check for debug false flag and pick the latest model
                const model_obj = res.results.at(-1)
                this.model.model_id = model_obj['id']
                this.model.model_name = model_obj['name']
            })
        },
        modelDownload() {
            this.downloading=true
            ModelsApi.downloadModel(
                this.projectStore.getProjectInfo.id,
                this.model.model_id
            ).then(res => {
                const blob = new Blob([res.data], { type: 'application/zip' })
                const link = document.createElement('a')
                link.href = URL.createObjectURL(blob)
                link.download = 'model'
                link.click()
                URL.revokeObjectURL(link.href)
                this.downloading=false
            }).catch((err) => {
                console.log(err);
                this.downloading=false
            });
        }
    }
};


</script>