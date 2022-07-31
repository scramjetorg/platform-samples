'use strict'
import Parser from 'rss-parser';
import axios from 'axios';

const parser = new Parser();

/**
 * Get links from RSS Feed
 * 
 * @param {string} url RSS URL
 * @returns {Array} Array of links
 */
async function getLinks(url: string) {
    const feed = await parser.parseURL(url);

    return feed.items.map(item => { return { title: item.title as string, url: item.link as string }; });
}

/**
 * Check if content matches keywords and calcualte weight of each keyword occurance.
 * 
 * @param {string} content Page content to be checked
 * @param {Array} keywords  Array of keywords and weights
 * @returns {Array} 
 */
function checkKeywords(content: string, keywords: Array<any>): Array<any> {

    const results: Array<any> = [];

    keywords.forEach(entry => {
        const regex = new RegExp(entry.word, 'g');

        const count = content.match(regex)?.length || 0;

        results.push({ word: entry.word, weight: count * entry.weight });
    });

    return results;
}

/**
 * Post message to slack
 * 
 * @param {string} title Title
 * @param {string} url URL
 * @param {Array} results Keywords
 */
async function postToSlack(slackWebhookUrl: string, title: string, url: string, results: Array<object>) {
    const text = `${title} ${url} ${JSON.stringify(results)}`;
    await axios.post(slackWebhookUrl, { text });
}

/**
 * Calucalte total score for given keywords 
 * 
 * @param keywords
 * @returns {number}
 */
function getScore(keywords: Array<any>) {
    return keywords.reduce((total, item) => total += item.weight, 0);
}

export { checkKeywords, getLinks, postToSlack, getScore };