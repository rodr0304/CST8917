# CST8917 - Assignment 1
## Serverless Computing: Critical Analysis

**Name:** Diniz Rodrigues Martins  
**Student Number:** 041179475  
**Course:** CST8917 – Serverless Applications  
**Date:** June 11, 2026

---

# Part 1 – Paper Summary

In their paper *Serverless Computing: One Step Forward, Two Steps Back*, Hellerstein et al. (2019) argue that serverless computing represents a significant advancement in cloud computing but also introduces several limitations that hinder its ability to support modern data-intensive applications. The authors acknowledge the benefits of Function-as-a-Service (FaaS), including automatic scaling, simplified deployment, reduced operational overhead, and a pay-per-use pricing model. However, they contend that these advantages come at the cost of losing capabilities that were already available in previous distributed computing systems. This concern is summarized by the paper’s title, which suggests that serverless computing has made progress in some areas while simultaneously moving backward in others.

One of the primary limitations identified by the authors is the strict execution time constraints imposed by many FaaS platforms. Early serverless services were designed for short-lived tasks and often enforced maximum execution durations. These restrictions make it difficult to run long-running analytics, machine learning training processes, and other computationally intensive workloads.

The paper also highlights communication and networking limitations. Functions are generally not directly addressable over the network, meaning they cannot communicate efficiently with one another using traditional distributed system techniques. Instead, communication often occurs through intermediary storage services such as object stores, databases, or message queues. This creates additional latency and reduces overall system efficiency. The authors describe this as an I/O bottleneck that can negatively impact performance.

Another criticism is the “data shipping” anti-pattern. In traditional distributed computing systems, it is often more efficient to move computation closer to where data resides. In serverless environments, however, data is frequently transferred to the function for processing. As datasets grow larger, the cost and latency associated with moving data become increasingly problematic.

The authors also discuss the lack of access to specialized hardware. Most first-generation serverless platforms did not provide access to GPUs, FPGAs, or other accelerators commonly used in artificial intelligence, machine learning, and high-performance computing workloads. This limitation prevents serverless platforms from supporting many advanced computational tasks.

Finally, the paper argues that distributed and stateful applications are difficult to implement in traditional FaaS environments. Because functions are designed to be stateless and short-lived, developers must rely on external services to manage application state and coordinate distributed tasks. This increases complexity and can reduce performance.

To address these challenges, the authors propose several characteristics for the future of cloud programming. First, they advocate for stronger support for stateful computation. Second, they recommend moving computation closer to data instead of moving data to code. Third, they encourage support for directly addressable services that can communicate efficiently. Additional recommendations include better support for distributed computing frameworks and access to specialized hardware resources. Overall, the paper calls for a new generation of cloud systems that preserve the benefits of serverless computing while eliminating its major limitations.

---

# Part 2 – Azure Durable Functions Deep Dive

## Orchestration Model

Azure Durable Functions extends the traditional Azure Functions model by introducing orchestration capabilities. A Durable Functions application typically consists of three components: client functions, orchestrator functions, and activity functions. Client functions start orchestration instances, orchestrator functions coordinate workflows, and activity functions perform individual units of work. Unlike traditional FaaS applications where functions operate independently, orchestrators can coordinate multiple activities, define dependencies, implement retries, and manage complex workflows. This model allows developers to build long-running business processes while maintaining the serverless programming experience. The orchestration model directly addresses one of the paper’s criticisms regarding the difficulty of coordinating complex distributed tasks using traditional stateless functions. Durable Functions provides a workflow layer that simplifies the development of distributed applications and reduces the need for custom coordination logic.

## State Management

One of the most significant innovations of Azure Durable Functions is its state management mechanism. Traditional serverless functions are stateless, requiring developers to store application state externally. Durable Functions uses event sourcing and checkpointing to persist workflow progress automatically. Every action performed by an orchestration is recorded in durable storage. When an orchestrator resumes execution, the runtime replays the execution history to reconstruct its current state. This process is known as deterministic replay. As a result, developers can write workflows that appear stateful while the platform manages persistence behind the scenes. This capability directly addresses the paper’s criticism that stateless functions make it difficult to build complex applications. Although state is still stored externally, the programming model provides a stateful abstraction that significantly simplifies workflow development.

## Execution Timeouts

Traditional serverless platforms often impose execution limits that make long-running workloads difficult to implement. Azure Durable Functions addresses this issue by separating orchestration logic from actual work execution. Orchestrator functions can manage workflows that run for hours, days, or even months because their state is continuously persisted between executions. The orchestration itself is not required to remain continuously active. Instead, the runtime restores progress whenever new events occur. However, activity functions remain subject to the execution limitations of the underlying Azure Functions hosting plan. Long-running computational tasks may still require decomposition into smaller activities. Therefore, Durable Functions significantly reduces the impact of execution timeouts for workflow coordination but does not completely eliminate execution constraints for individual compute-intensive operations.

## Communication Between Functions

The paper criticizes traditional serverless platforms for requiring communication through external storage systems. Durable Functions improves this situation by providing built-in coordination mechanisms between orchestrator and activity functions. Activity results are automatically returned to the orchestrator through the Durable Task Framework. Developers do not need to manually implement communication through databases, queues, or storage accounts. The runtime manages state transitions and event delivery transparently. Although Durable Functions still relies on underlying storage services to maintain reliability and persistence, the communication process is abstracted from the developer. This significantly reduces complexity and improves developer productivity. However, the underlying dependency on durable storage means that communication is not entirely free from the latency concerns identified in the paper.

## Parallel Execution (Fan-Out/Fan-In)

Durable Functions supports the fan-out/fan-in pattern, which is commonly used in distributed computing. In this model, an orchestrator creates multiple activity functions that execute in parallel. Once all activities complete, the orchestrator aggregates the results and continues execution. This pattern enables efficient parallel processing of independent tasks such as file processing, data analysis, and large-scale batch operations. By simplifying parallel execution, Durable Functions addresses some of the paper’s concerns regarding distributed computing challenges. Developers can implement distributed workloads using a relatively simple programming model without manually managing synchronization and coordination. However, Durable Functions is not a replacement for large-scale distributed processing frameworks such as Apache Spark, meaning some limitations still remain for highly data-intensive applications.

---

# Part 3 – Critical Evaluation

Although Azure Durable Functions addresses many limitations identified by Hellerstein et al., several criticisms remain unresolved or only partially resolved.

The first unresolved limitation is the data shipping problem. The paper argues that modern cloud platforms should move computation closer to where data resides rather than repeatedly moving large datasets across the network. Durable Functions improves workflow coordination, but it does not fundamentally change data locality. Activity functions still retrieve data from external storage systems, process it, and often write results back to storage. For large-scale analytics workloads, the cost and latency associated with data movement remain significant. Therefore, Durable Functions improves orchestration but does not eliminate the underlying architectural issue described by the authors.

The second unresolved limitation is the lack of direct access to specialized hardware. The paper emphasizes the importance of GPUs, FPGAs, and other accelerators for machine learning and high-performance computing. Durable Functions primarily focuses on workflow management rather than computational capabilities. While Azure as a cloud platform offers GPU-enabled services, Durable Functions itself does not provide a mechanism that fundamentally changes how serverless applications access specialized hardware. Consequently, workloads that require intensive machine learning training or scientific computation are still better suited for alternative cloud services.

Despite these limitations, Azure Durable Functions represents meaningful progress toward the vision proposed by the authors. The introduction of orchestration, state management, checkpointing, and workflow persistence significantly improves the practicality of serverless applications. Many of the challenges associated with stateless execution, workflow coordination, and long-running processes have been addressed through a developer-friendly programming model.

However, Durable Functions should be viewed primarily as an evolution of serverless computing rather than a complete solution to all of its fundamental limitations. The platform provides abstractions that make serverless development easier and more powerful, but many of the underlying architectural constraints remain present. Communication still depends on durable storage. Data locality challenges still exist. Specialized hardware support remains outside the scope of the framework. In addition, Durable Functions does not replace dedicated distributed computing platforms for extremely large-scale data processing.

My overall verdict is that Azure Durable Functions represents substantial progress in the direction envisioned by Hellerstein et al. It demonstrates how serverless platforms can evolve beyond simple stateless functions and support more sophisticated application architectures. Nevertheless, it does not fully realize the future cloud programming model proposed in the paper. Instead, it provides practical workarounds and abstractions that reduce the impact of several limitations while leaving some fundamental challenges unresolved. As a result, Durable Functions should be considered an important step forward for serverless computing, but not the final destination envisioned by the authors.

---

# References

Hellerstein, J. M., Faleiro, J., Gonzalez, J. E., Schleier-Smith, J., Sreekanti, V., Tumanov, A., & Wu, C. (2019). *Serverless Computing: One Step Forward, Two Steps Back*. Conference on Innovative Data Systems Research (CIDR).  
https://www.cidrdb.org/cidr2019/papers/p119-hellerstein-cidr19.pdf

Microsoft Learn. *Durable Functions Overview*.  
https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-overview

Microsoft Learn. *Durable Orchestrations*.  
https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-orchestrations

Microsoft Learn. *Durable Functions Bindings*.  
https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-bindings

Microsoft Learn. *Fan-out/Fan-in Scenario in Durable Functions*.  
https://learn.microsoft.com/azure/azure-functions/durable/durable-functions-cloud-backup

---

AI Disclosure Statement

ChatGPT was used to assist with understanding the research paper, organizing ideas, improving writing clarity, and generating draft content. All information was reviewed, verified against the original paper and Microsoft documentation, and edited by the author before submission.
