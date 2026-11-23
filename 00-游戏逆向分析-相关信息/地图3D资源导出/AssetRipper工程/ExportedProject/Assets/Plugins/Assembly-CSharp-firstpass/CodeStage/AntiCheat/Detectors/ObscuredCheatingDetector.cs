using System;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace CodeStage.AntiCheat.Detectors
{
	[DisallowMultipleComponent]
	public class ObscuredCheatingDetector : ACTkDetectorBase
	{
		internal const string ComponentName = "Obscured Cheating Detector";

		internal const string FinalLogPrefix = "[ACTk] Obscured Cheating Detector: ";

		private static int instancesInScene;

		public double doubleEpsilon;

		public float floatEpsilon;

		public float vector2Epsilon;

		public float vector3Epsilon;

		public float quaternionEpsilon;

		public static ObscuredCheatingDetector Instance { get; private set; }

		private static ObscuredCheatingDetector GetOrCreateInstance => null;

		internal static bool ExistsAndIsRunning => false;

		public static ObscuredCheatingDetector AddToSceneOrGetExisting()
		{
			return null;
		}

		public static void StartDetection()
		{
		}

		public static void StartDetection(Action callback)
		{
		}

		public static void StopDetection()
		{
		}

		public static void Dispose()
		{
		}

		private ObscuredCheatingDetector()
		{
		}

		private void Awake()
		{
		}

		protected override void OnDestroy()
		{
		}

		private void OnLevelWasLoadedNew(Scene scene, LoadSceneMode mode)
		{
		}

		private void StartDetectionInternal(Action callback)
		{
		}

		protected override void StartDetectionAutomatically()
		{
		}

		protected override void DisposeInternal()
		{
		}
	}
}
