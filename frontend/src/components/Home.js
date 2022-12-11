import { useState, useEffect } from "react";
import { useFormik } from "formik";
import {
    Box,
    Button,
    Flex,
    FormControl,
    FormLabel,
    VStack,
    Select,
    Stack,
    Text,
    Highlight,
    Table,
    Thead,
    Tbody,
    Tr,
    Th,
    Td,
    TableContainer,
    StackDivider,
    useToast,
    Textarea,
} from "@chakra-ui/react";
import axios from "axios";

import { ENDPOINTS, ML_MODELS, PREDICT, TAGS } from "../api/constants";

const ANONYMIZE = "anonymize"

export default function Home() {

    const [endpoints, setEndpoints] = useState(null);
    const [models, setModels] = useState(null);
    const [anonyId, setAnonyId] = useState(null);
    const [anonyModel, setAnonyModel] = useState(null);
    const [anonyTags, setAnonyTags] = useState(["ALL"]);

    const [anonyOutput, setAnonyOutput] = useState(null);
    const [lookupTable, setLookupTable] = useState(null);
    const [highlights, setHighlights] = useState([]);

    const [loading, setLoading] = useState(false)

    const toast = useToast();

    const formik = useFormik({
        initialValues: {
            model: "0",
            sentence: "Albert Einstein was born in Germany and lived in England",
            tag: "",
        },
        onSubmit: (values) => {
            handleSubmit(values);
        }
    });

    const fetchTags = async () => {
        const modelIdx = formik.values.model;        
        const url = TAGS + ANONYMIZE + "/" + modelIdx;
        const result = await axios.get(url);        
        setAnonyTags(result.data.tags);
        formik.values.tag = result.data.tags[0]
    }


    useEffect(() => {
        axios.get(ENDPOINTS).then((response) => {
            const endpoints_data = response.data;
            endpoints_data.forEach((data) => {
                if (data.name === ANONYMIZE) {
                    setAnonyId(data.id);
                }
            });

            setEndpoints(endpoints_data);
        });
    }, []);

    useEffect(() => {
        axios.get(ML_MODELS).then((response) => {
            setModels(response.data);
        });
    }, []);

    useEffect(() => {
        if (models === null) return;
        if (anonyId === null) return;

        let anonyModelData = []
        models.forEach((data) => {
            if (data.parent_endpoint === anonyId) {
                anonyModelData.push(data);
            }
        });        
        
        setAnonyModel(anonyModelData);
    }, [endpoints, models, anonyId]);

    useEffect(() => {        
        fetchTags();
    }, [formik.values.model])

    const getModelOptions = () => {
        if (anonyModel == null) return;
        return anonyModel.map((model, index) => {
            return <option
                key={model.id}
                value={index}
            >
                {model.name}
            </option>
        });
    };

    const getTagOptions = () => {
        if (anonyTags == null) return;
        return anonyTags.map((tag) => {
            return <option
                key={tag}
                value={tag}
            >
                {tag}
            </option>
        });
    };


    const handleSubmit = (values) => {
        const url = PREDICT + ANONYMIZE + "/" + values.model + "/" + values.tag;

        var data = JSON.stringify(values.sentence)

        var config = {
            method: 'post',
            url: url,
            headers: {
                'Content-Type': 'application/json'
            },
            data: data
        };

        setLoading(true);

        axios(config).then(function (response) {
            const data = response.data;
            // console.log(data)
            
            if(data.status !== "OK") {
                toast({
                    title: 'Error',
                    description: data.message,
                    status: 'error',
                    duration: 3000,
                    isClosable: true,
                })
                setLoading(false)
                return;
            }
            
            setAnonyOutput(data.prediction)


            if (data.lookup !== "") {                
                for (const key in data.lookup) {
                    const words = data.lookup[key].split(" ");
                    for(const idx in words) {
                        setHighlights(oldArray => [...oldArray, words[idx]]);
                    }
               }
                
                setLookupTable(data.lookup);
            }

            setLoading(false);
        }).catch(function (error) {
            console.log(error);
            setLoading(false);
        });
    }

    return (
        <Flex bg="gray.100" align="center" justify="center" minHeight="100vh">
            <VStack spacing={4} align="flex-start">

                <Box bg="white" p={8} rounded="md" w="50vw">
                    <form onSubmit={formik.handleSubmit}>
                        <VStack spacing={6} align="flex-start">
                            <FormControl>
                                <FormLabel>Select Anonymizer Model</FormLabel>
                                <Select
                                    name="model"
                                    id="model"
                                    variant="filled"
                                    onChange={formik.handleChange}
                                >
                                    {getModelOptions()}
                                </Select>
                            </FormControl>

                            <FormControl>
                                <FormLabel htmlFor="email">Sentence to Anonymize</FormLabel>
                                <Textarea
                                    id="sentence"
                                    name="sentence"
                                    onChange={formik.handleChange}
                                    value={formik.values.sentence}
                                />
                            </FormControl>

                            <FormControl>
                                <FormLabel>Select Tag</FormLabel>
                                <Select
                                    name="tag"
                                    id="tag"
                                    variant="filled"
                                    onChange={formik.handleChange}
                                >
                                    {getTagOptions()}
                                </Select>
                            </FormControl>
                            <Button type="submit" colorScheme="purple" width="full" isLoading={loading}>
                                Submit
                            </Button>
                        </VStack>
                    </form>
                </Box>

                {anonyOutput &&
                    <Box bg="white" p={8} rounded="md" w="50vw">
                        <Stack spacing={3}   divider={<StackDivider borderColor='black.100' />}>
                            <Text as="b" fontSize='lg'>Anonymized Sentence</Text>
                            <Text fontSize='md'>
                                <Highlight fontSize='md' query={highlights} 
                                styles={{ px: '2', py: '1', rounded: 'full', bg: 'red.100' }}
                                >
                                    {anonyOutput}    
                                </Highlight>
                            </Text>

                            {lookupTable &&
                            <TableContainer>
                                <Table variant='striped' colorScheme='purple'>
                                    <Thead>
                                    <Tr>
                                        <Th>Original Word</Th>
                                        <Th>Anonymized Word</Th>
                                    </Tr>
                                    </Thead>
                                    <Tbody>
                                    {Object.keys(lookupTable).map((key, index) => ( 
                                        <Tr key={index}>
                                            <Td>{key}</Td>
                                            <Td>{lookupTable[key]}</Td>
                                        </Tr>
                                    ))}
                                    </Tbody>
                                </Table>
                            </TableContainer>
                            }
                        </Stack>
                    </Box>
                }
            </VStack>

        </Flex >
    );
}