using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public static class ExpandUtil
{
	private static byte[] keyBytes;

	private static byte[] ivBytes;

	public static bool IsTimeValidAndEnd(this float time)
	{
		return false;
	}

	public static int GetSign(this float value)
	{
		return 0;
	}

	public static Vector3 ClearDirY(this Vector3 dir)
	{
		return default;
	}

	public static float DistanceToRay(this Vector3 point, Ray ray)
	{
		return 0f;
	}

	public static bool KnifeAtkCheck(this Collider collider, Ray ray, float rad)
	{
		return false;
	}

	public static bool IsInRayRad(this Vector3 point, Ray ray, float rad)
	{
		return false;
	}

	public static bool IsSphereInRayRad(this Vector3 center, float radius, Ray ray, float rad)
	{
		return false;
	}

	public static bool IsInRayRad(this BoxCollider boxCollider, Ray ray, float rad)
	{
		return false;
	}

	public static bool IsInRayRad(this CapsuleCollider capsuleCollider, Ray ray, float rad)
	{
		return false;
	}

	public static bool IsInRayRad(this SphereCollider sphereCollider, Ray ray, float rad)
	{
		return false;
	}

	public static bool IsEnemy(this Entity entity, Entity other)
	{
		return false;
	}

	public static bool IsSameTeam(this Team team, Team otherTeam)
	{
		return false;
	}

	public static Vector3 DirToRot(Vector3 dir)
	{
		return default;
	}

	public static float ClampIn180Degrees(float angle)
	{
		return 0f;
	}

	public static float GetDeltaXAngle(Vector3 fromDir, Vector3 toDir)
	{
		return 0f;
	}

	public static float GetDeltaYAngle(Vector3 fromDir, Vector3 toDir)
	{
		return 0f;
	}

	public static string GetSuffix(this Team team)
	{
		return null;
	}

	public static string GetSingleChar(this CharacterModel.MoveDirection dir)
	{
		return null;
	}

	public static string AddSuffix(this CharacterModel.MoveDirection dir, string head)
	{
		return null;
	}

	public static void Synchronize(this Animator thisAnimator, Animator otherAnimator)
	{
	}

	public static void ApplySpriteSize(this RectTransform rect, Sprite sprite)
	{
	}

	public static string Load(this string source, int head)
	{
		return null;
	}

	public static string StringPack(string input)
	{
		return null;
	}

	public static string StringUnpack(string cipherStr)
	{
		return null;
	}

	public static bool IsMouseInArea(Vector4 area)
	{
		return false;
	}

	public static int GetLevel(int exp, int[] expPerLevel)
	{
		return 0;
	}

	public static void SetSpriteSize(this RectTransform rect, Sprite spr)
	{
	}

	public static void RefreshValue(this Dropdown dropdown, int newValue)
	{
	}

	public static void SetAllTransformScale(this Transform transform, Vector3 scale)
	{
	}

	public static void TransportList<T>(List<T> fromList, List<T> toList, T target)
	{
	}

	public static T GetLastElement<T>(this List<T> list)
	{
		return default;
	}
}
