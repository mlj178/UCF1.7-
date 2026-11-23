using CodeStage.AntiCheat.Detectors;
using UnityEngine;

namespace CodeStage.AntiCheat.Examples
{
	public class DetectorsExamples : MonoBehaviour
	{
		internal bool injectionDetected;

		internal bool speedHackDetected;

		internal bool wrongTimeDetected;

		internal bool timeCheatingDetected;

		internal bool obscuredTypeCheatDetected;

		internal bool wallHackCheatDetected;

		public void OnSpeedHackDetected()
		{
		}

		public void OnTimeCheatingDetected()
		{
		}

		public void OnInjectionDetected()
		{
		}

		public void OnInjectionDetectedWithCause(string cause)
		{
		}

		public void OnObscuredTypeCheatingDetected()
		{
		}

		public void OnWallHackDetected()
		{
		}

		public void OnTimeCheatChecked(TimeCheatingDetector.CheckResult checkResult, TimeCheatingDetector.ErrorKind errorKind)
		{
		}

		private void Start()
		{
		}

		private void SpeedHackDetectorExample()
		{
		}

		private void InjectionDetectorExample()
		{
		}

		private void ObscuredCheatingDetectorExample()
		{
		}

		private void TimeCheatingDetectorExample()
		{
		}

		internal void ForceTimeCheatingDetectorCheck()
		{
		}
	}
}
