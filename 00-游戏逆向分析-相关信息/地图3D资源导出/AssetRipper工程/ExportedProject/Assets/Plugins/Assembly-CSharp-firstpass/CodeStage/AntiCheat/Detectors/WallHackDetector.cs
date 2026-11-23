using System;
using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace CodeStage.AntiCheat.Detectors
{
	[DisallowMultipleComponent]
	public class WallHackDetector : ACTkDetectorBase
	{
		internal const string ComponentName = "WallHack Detector";

		internal const string FinalLogPrefix = "[ACTk] WallHack Detector: ";

		private const string ServiceContainerName = "[WH Detector Service]";

		private const string WireframeShaderName = "Hidden/ACTk/WallHackTexture";

		private const int ShaderTextureSize = 4;

		private const int RenderTextureSize = 4;

		private readonly Vector3 rigidPlayerVelocity;

		private static int instancesInScene;

		private readonly WaitForEndOfFrame waitForEndOfFrame;

		[SerializeField]
		private bool checkRigidbody;

		[SerializeField]
		private bool checkController;

		[SerializeField]
		private bool checkWireframe;

		[SerializeField]
		private bool checkRaycast;

		public int wireframeDelay;

		public int raycastDelay;

		public Vector3 spawnPosition;

		public byte maxFalsePositives;

		private GameObject serviceContainer;

		private GameObject solidWall;

		private GameObject thinWall;

		private Camera wfCamera;

		private MeshRenderer foregroundRenderer;

		private MeshRenderer backgroundRenderer;

		private Color wfColor1;

		private Color wfColor2;

		private Shader wfShader;

		private Material wfMaterial;

		private Texture2D shaderTexture;

		private Texture2D targetTexture;

		private RenderTexture renderTexture;

		private int whLayer;

		private int raycastMask;

		private Rigidbody rigidPlayer;

		private CharacterController charControllerPlayer;

		private float charControllerVelocity;

		private byte rigidbodyDetections;

		private byte controllerDetections;

		private byte wireframeDetections;

		private byte raycastDetections;

		private bool wireframeDetected;

		private readonly RaycastHit[] rayHits;

		public bool CheckRigidbody
		{
			get
			{
				return false;
			}
			set
			{
			}
		}

		public bool CheckController
		{
			get
			{
				return false;
			}
			set
			{
			}
		}

		public bool CheckWireframe
		{
			get
			{
				return false;
			}
			set
			{
			}
		}

		public bool CheckRaycast
		{
			get
			{
				return false;
			}
			set
			{
			}
		}

		public static WallHackDetector Instance { get; private set; }

		private static WallHackDetector GetOrCreateInstance => null;

		public static WallHackDetector AddToSceneOrGetExisting()
		{
			return null;
		}

		public static void StartDetection()
		{
		}

		public static void StartDetection(Action callback)
		{
		}

		public static void StartDetection(Action callback, Vector3 spawnPosition)
		{
		}

		public static void StartDetection(Action callback, Vector3 spawnPosition, byte maxFalsePositives)
		{
		}

		public static void StopDetection()
		{
		}

		public static void Dispose()
		{
		}

		private WallHackDetector()
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

		private void FixedUpdate()
		{
		}

		private void Update()
		{
		}

		private void StartDetectionInternal(Action callback, Vector3 servicePosition, byte falsePositivesInRow)
		{
		}

		protected override void StartDetectionAutomatically()
		{
		}

		protected override void PauseDetector()
		{
		}

		protected override bool ResumeDetector()
		{
			return false;
		}

		protected override void StopDetectionInternal()
		{
		}

		protected override void DisposeInternal()
		{
		}

		private void UpdateServiceContainer()
		{
		}

		private IEnumerator InitDetector()
		{
			return null;
		}

		private void StartRigidModule()
		{
		}

		private void StartControllerModule()
		{
		}

		private void StartWireframeModule()
		{
		}

		private void ShootWireframeModule()
		{
		}

		private IEnumerator CaptureFrame()
		{
			return null;
		}

		private void StartRaycastModule()
		{
		}

		private void ShootRaycastModule()
		{
		}

		private void StopRigidModule()
		{
		}

		private void StopControllerModule()
		{
		}

		private void StopWireframeModule()
		{
		}

		private void StopRaycastModule()
		{
		}

		private void InitRigidModule()
		{
		}

		private void InitControllerModule()
		{
		}

		private void UninitRigidModule()
		{
		}

		private void UninitControllerModule()
		{
		}

		private bool Detect()
		{
			return false;
		}

		private static Color32 GenerateColor()
		{
			return default;
		}

		private static bool ColorsSimilar(Color32 c1, Color32 c2, int tolerance)
		{
			return false;
		}
	}
}
