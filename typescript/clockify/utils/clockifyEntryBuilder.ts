/* eslint-disable no-async-promise-executor */
/* eslint-disable max-len */
import * as data from "../data.json";
import { ClockifyClient } from "./clockify";

export class ClockifyEntryBuilder {
    clockifyClient = new ClockifyClient();
    day:Date;

    setDate(day:Date) {
        this.day = day;
        this.day.setMinutes(0);
        this.day.setSeconds(0);
        this.day.setMilliseconds(0);
    }
    setApiKey(apiKey:string){
        this.clockifyClient.setApiKey(apiKey);
    }
    setTime(time:number):Date {
        return new Date(this.day.setHours(time));
    }
    async sendRequest():Promise<string> {
        const start = this.setTime(data.startHour);

        return new Promise(async (res, rej) => {
            try {
                switch (this.day.getDay()) {
                    case 0:
                        await this.clockifyClient.sendRequest({ startTime:this.setTime(data.sunStartHour), endTime:this.setTime(data.sunEndHour), projectId:data.sunProjectId });
                        res("request sent for Sunday");
                        break;
                    case 6:
                        await this.clockifyClient.sendRequest({ startTime:this.setTime(data.satStartHour), endTime:this.setTime(data.satEndHour), projectId:data.satProjectId });
                        res("request sent for Saturday");
                        break;
                    default:
                        const end = this.setTime(data.endHour);

                        await this.clockifyClient.sendRequest({ startTime:start, endTime:end, projectId:data.weekDayProjectId })
                            .then((response) => res(response))
                            .catch((error) => rej(error));

                        break;
                }
            } catch (error) {
                rej(error);
            }
        });
    }
}
