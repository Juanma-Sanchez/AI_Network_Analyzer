# AI Network Analyzer

This repository contains an experimental network analyzer that takes traffic metrics from a monitoring system and uses AI and/or statistics to determine wether the traffic per interface is anomalus or not based on previous metrics.

![AI_Network_Analyzer Concept](resources/images/Concept.jpg)

## AI Analyzer

The AI analyzer obtains a certain amount of traffic metrics and then sends them to Google Gemini for it to analyze and return an structured response.

Using an AI for this analysis allows us to obtain information without specifically programming an algorithm to obtain, like wether an entire device might be down or if a Man in the Middel attack is being performed in our network. However the output may be unreliable and the more information we provide in the system instructions, the more likely is the LLM to succeed.

## Threshold analyzer

The threshold analyzer takes information from the traffic metrics per interface to extrapolate a gaussian distribution and determine the upper and lower thresholds of a 95% probability confidence interval.

TODO: add discrete data to gaussian distribution with confidence interval graphic

Once there is enough data, it evaluates every trace against both thresholds and determines wether the traffic is normal, below the lower threshold or above the upper one. If the traffic is normal the data used to extrapolate the gaussian distribution is updated.

This procedure does not take into account the rest of the network, but it provides a concrete analysis of the traffic.

### Installation

Blabla

### Usage

Blabla

## Example

Blabla

### Installation

### Usage

### Performance evaluation

TODO include three abnormal traffic scenarios: link down, device down and Man in the Middle attack (simulated through proxy configuration).

## Conclussions

Might remove this
