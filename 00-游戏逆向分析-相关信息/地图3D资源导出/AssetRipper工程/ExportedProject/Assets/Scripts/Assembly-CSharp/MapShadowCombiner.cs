using System.Collections.Generic;
using UnityEngine;

public class MapShadowCombiner : MonoBehaviour
{
	[SerializeField]
	private MeshFilter oneSideShadow;

	[SerializeField]
	private MeshFilter twoSideShadow;

	[SerializeField]
	private MeshRenderer[] mapShadowCasters;

	private List<MeshFilter> oneSideMesh;

	private List<MeshFilter> twoSideMesh;

	private void Awake()
	{
	}

	private void CheckMeshRender(MeshRenderer mr)
	{
	}

	private void Combine(List<MeshFilter> input, MeshFilter output)
	{
	}
}
